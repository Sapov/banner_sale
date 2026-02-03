from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from django.conf import settings

User = get_user_model()

class StatusOrder(models.TextChoices):

    PREPARING = "PREPARING", "ГОТОВИТЬСЯ"
    DECORATED = "DECORATED", "ОФОРМЛЕН"
    MANAGER = "MANAGER", "Менеджер"
    AT_WORK = "AT WORK", "В РАБОТЕ"
    DELIVERY = "DELIVERY", "В ДОСТАВКЕ"
    READY = "READY", "ГОТОВ"
    CLOSED = "CLOSED", "ЗАКРЫТ"


    class Meta:
        verbose_name_plural = "Статусы ЗАКАЗА"
        verbose_name = "Статус"



class Order(models.Model):
    # delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, verbose_name='Доставка', null=True, default=1)
    total_price = models.FloatField(max_length=10, null=True, help_text="Стоимость заказа",
                                    verbose_name="Общая Стоимость", blank=True, )
    cost_total_price = models.FloatField(
        max_length=10,
        null=True,
        help_text="Себестоимость заказа",
        verbose_name="Общая Себестоимость",
        blank=True,
    )

    paid = models.BooleanField(verbose_name="Заказ оплачен", default=False)
    date_complete = models.DateTimeField(
        verbose_name="Дата готовности заказа",
        help_text="Введите дату к которой нужен заказ",
        null=True,
        blank=True,
    )
    comments = models.TextField(verbose_name="Комментарии к заказу", blank=True)
    status = models.CharField(max_length=24, choices=StatusOrder.choices, default=StatusOrder.PREPARING)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(  # переименовать в юзера!!!!!
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Заказчик",
        default=1,
    )
    order_arhive = models.FileField(upload_to=f"arhive/{id}", null=True, blank=True)
    order_pdf_file = models.FileField(upload_to=f"orders/", null=True, blank=True)
    pay_link = models.TextField(verbose_name='Ссылка для оплаты', null=True, blank=True)

    def __str__(self):
        return f"Заказ № {self.id}"

    class Meta:
        verbose_name_plural = "Заказы"
        verbose_name = "Заказ"

    def get_absolute_url(self):
        return reverse("orders:add_file_in_order", args=[self.id])


from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import base64


class Banner(models.Model):
    GROMMET_CHOICES = [
        ('perimeter', 'По периметру'),
        ('corners', 'По углам'),
        ('none', 'Без люверсов'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Заказчик",
    )
    width = models.FloatField(default=0, verbose_name="Ширина", help_text="Указывается в см.")
    height = models.FloatField(default=0, verbose_name="Высота", help_text="Указывается в см.")
    banner_text = models.CharField(max_length=50, verbose_name='Текст баннера')
    banner_phone = models.CharField(max_length=15, verbose_name='Телефон')
    background_color = models.CharField(max_length=10, verbose_name='Цвет фона')
    font_color = models.CharField(max_length=10, verbose_name='Цвет букв')
    grommet = models.CharField(
        max_length=20,
        choices=GROMMET_CHOICES,
        default='none',
        verbose_name='Люверсы'
    )
    quantity = models.IntegerField(default=1, help_text="Введите количество", verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    image = models.ImageField(
        upload_to='banners/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Изображение баннера"
    )
    image_base64 = models.TextField(blank=True, verbose_name="Base64 изображения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")

    def __str__(self):
        return f"Баннер {self.id} - {self.width}x{self.height}см"

    def save_image_from_base64(self, base64_string):
        """Сохраняет изображение из base64 строки"""
        if not base64_string:
            return

        # Удаляем префикс data:image/png;base64,
        if 'base64,' in base64_string:
            format, imgstr = base64_string.split(';base64,')
            ext = format.split('/')[-1]
        else:
            imgstr = base64_string
            ext = 'png'

        # Декодируем base64
        data = base64.b64decode(imgstr)

        # Создаем изображение в памяти
        image = Image.open(BytesIO(data))

        # Сохраняем в поле image
        filename = f'banner_{self.id}_{self.created_at.strftime("%Y%m%d_%H%M%S")}.{ext}'
        self.image.save(filename, ContentFile(data), save=False)

        # Сохраняем base64 в отдельное поле (опционально)
        self.image_base64 = base64_string

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Ордер")
    product = models.ForeignKey(
        Banner, on_delete=models.CASCADE, verbose_name="Баннер"
    )
    price_per_item = models.FloatField(
        max_length=100, help_text="За 1 шт.", verbose_name="Стоимость шт.", blank=True
    )
    cost_price_per_item = models.FloatField(
        max_length=100,
        help_text="За 1 шт.",
        verbose_name="Себестоимость шт.",
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(
        default=1, help_text="Введите количество", verbose_name="Количество"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Себестоимость Итого",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )  # date created
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Изменено"
    )  # date update

    class Meta:
        verbose_name_plural = "Товары в заказе"
        verbose_name = "Товар в заказе"


class BannerOrder(models.Model):
    GROMMET_CHOICES = [
        ('perimeter', 'По периметру'),
        ('corners', 'По углам'),
        ('none', 'Без люверсов'),
    ]

    width = models.IntegerField(verbose_name="Ширина (мм)")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.IntegerField(verbose_name="Высота (мм)")
    text = models.CharField(max_length=255, verbose_name="Текст баннера")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    bg_color = models.CharField(max_length=7, verbose_name="Цвет фона")
    text_color = models.CharField(max_length=7, verbose_name="Цвет текста")
    grommet_type = models.CharField(max_length=20, choices=GROMMET_CHOICES, verbose_name="Тип люверсов")
    image = models.ImageField(upload_to='banner_orders/%Y/%m/%d/', verbose_name="Изображение баннера")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Баннер {self.id}-{self.width}x{self.height} - {self.created_at}"

