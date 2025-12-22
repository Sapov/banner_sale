from django.contrib.auth.models import User
from django.db import models

from users.models import CustomUser


class StatusOrder(models.Model):

    PREPARING = "PREPARING", "ГОТОВИТЬСЯ"
    DECORATED = "DECORATED", "ОФОРМЛЕН"
    MANAGER = "MANAGER", "Менеджер"
    AT_WORK = "AT WORK", "В РАБОТЕ"
    DELIVERY = "DELIVERY", "В ДОСТАВКЕ"
    READY = "READY", "ГОТОВ"
    CLOSED = "CLOSED", "ЗАКРЫТ"

    name = models.CharField(max_length=48, verbose_name="Статус заказа")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

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
    organisation_payer = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        verbose_name="Организация плательщик",
        help_text="Выберите организацию плательщик",
        null=True,
        blank=True,
        default=1
    )
    paid = models.BooleanField(verbose_name="Заказ оплачен", default=False)
    date_complete = models.DateTimeField(
        verbose_name="Дата готовности заказа",
        help_text="Введите дату к которой нужен заказ",
        null=True,
        blank=True,
    )
    comments = models.TextField(verbose_name="Комментарии к заказу", blank=True)
    status = models.ForeignKey(
        StatusOrder, on_delete=models.CASCADE, verbose_name="Статус заказа", default=1
    )
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



class Banner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    width = models.FloatField(default=0, verbose_name="Ширина", help_text="Указывается в см.")
    length = models.FloatField(default=0, verbose_name="Длина", help_text="Указывается в см.")
    banner_text = models.CharField(max_length=50, verbose_name='Текст баннера')
    banner_phone = models.CharField(max_length=15, verbose_name='Телефон')
    background_color = models.CharField(max_length=10, verbose_name='цвет фона')
    font_color = models.CharField(max_length=10, verbose_name='цвет букв')
    grommet = models.ForeignKey('self',on_delete = models.PROTECT,related_name = 'Люверсы')
    quantity = models.IntegerField(default=1, help_text="Введите количество", verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")  # date created




class Grommet(models.Model):
    type_grommet = models.CharField(max_length = 100, verbose_name = 'grommet')


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
