from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.utils import timezone
import json
import base64
from .models import Banner


class BannerGeneratorView(View):
    """View для генерации и сохранения баннеров"""

    def get(self, request):
        """
        Отображает страницу генератора баннеров.
        """
        context = {
            'title': 'Заказать баннер "ПРОДАЮ"',
            'page_name': 'banner_generator',
        }

        return render(request, 'orders/banner_generator.html', context)

    def post(self, request):
        """
        Сохраняет баннер с изображением в базу данных.
        """
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST
                if 'image_data' in request.FILES:
                    data['image'] = request.FILES['image_data']

            # Получаем данные из запроса
            width_mm = float(data.get('width', 900))
            height_mm = float(data.get('height', 400))
            text = data.get('text', '')
            phone = data.get('phone', '')
            bg_color = data.get('bgColor', '#ff0000')
            text_color = data.get('textColor', '#ffffff')
            grommet_type = data.get('grommetType', 'none')
            image_data = data.get('image', '')  # base64 строка

            # Преобразуем мм в см (в модели размеры в см)
            width_cm = width_mm / 10
            height_cm = height_mm / 10

            # Создаем объект баннера
            banner = Banner.objects.create(
                user=request.user,
                width=width_cm,
                height=height_cm,
                banner_text=text,
                banner_phone=phone,
                background_color=bg_color,
                font_color=text_color,
                grommet=grommet_type,
                quantity=1,
                price=self.calculate_price(width_cm, height_cm, grommet_type)
            )

            # Сохраняем изображение если есть base64 данные
            if image_data:
                self.save_base64_image(banner, image_data)

            return JsonResponse({
                'status': 'success',
                'message': 'Баннер успешно сохранен!',
                'banner_id': banner.id,
                'banner_url': banner.image.url if banner.image else '',
                'redirect_url': f'/banners/{banner.id}/'  # URL для просмотра сохраненного баннера
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Ошибка при сохранении: {str(e)}'
            }, status=400)

    def calculate_price(self, width_cm, height_cm, grommet_type):
        """
        Рассчитывает цену баннера.
        Можно настроить свою логику расчета.
        """
        area = width_cm * height_cm  # площадь в см²
        price_per_cm2 = 0.01  # цена за 1 см²

        base_price = area * price_per_cm2

        # Доплата за люверсы
        if grommet_type == 'perimeter':
            base_price += 100  # например, +100 руб за люверсы по периметру
        elif grommet_type == 'corners':
            base_price += 50  # +50 руб за угловые люверсы

        return base_price

    def save_base64_image(self, banner, base64_string):
        """Сохраняет изображение из base64 строки"""
        if not base64_string or 'base64,' not in base64_string:
            return

        try:
            # Удаляем префикс data:image/png;base64,
            format, imgstr = base64_string.split(';base64,')
            ext = format.split('/')[-1]  # получаем расширение (png, jpeg и т.д.)

            # Декодируем base64
            data = base64.b64decode(imgstr)

            # Создаем имя файла
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            filename = f'banner_{banner.id}_{timestamp}.{ext}'

            # Сохраняем изображение
            banner.image.save(filename, ContentFile(data), save=True)

            # Сохраняем base64 в отдельное поле (опционально)
            banner.image_base64 = base64_string
            banner.save()

        except Exception as e:
            print(f"Ошибка при сохранении изображения: {e}")


# views.py
from django.views.generic import DetailView


class BannerDetailView(LoginRequiredMixin, DetailView):
    model = Banner
    template_name = 'banner_detail.html'
    context_object_name = 'banner'

    def get_queryset(self):
        # Пользователь может видеть только свои баннеры
        return Banner.objects.filter(user=self.request.user)