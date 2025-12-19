from django.contrib.auth.models import User
from django.db import models

from users.models import CustomUser


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