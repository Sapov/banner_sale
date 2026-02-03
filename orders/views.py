from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Banner
from django.views.decorators.csrf import csrf_exempt



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

        return render(request, 'orders/create_banner.html', context)

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



# views.py
from django.views.generic import DetailView, ListView


class BannerDetailView(LoginRequiredMixin, DetailView):
    model = Banner
    template_name = 'banner_detail.html'
    context_object_name = 'banner'

    def get_queryset(self):
        # Пользователь может видеть только свои баннеры
        return Banner.objects.filter(user=self.request.user)


from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import BannerOrder
from .forms import BannerOrderForm



# Или с использованием Django форм:
@csrf_exempt
def order_banner(request):
    if request.method == 'POST':
        form = BannerOrderForm(request.POST, request.FILES)

        if form.is_valid():
            order = form.save()

            # Если нужно обработать изображение из canvas
            if 'image' in request.FILES:
                order.image = request.FILES['image']
                order.save()

            return JsonResponse({
                'success': True,
                'order_id': order.id
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })

    return JsonResponse({'error': 'Invalid request method'}, status=400)


class Banners_ListView(LoginRequiredMixin, ListView):
    model = BannerOrder
    template_name = 'orders/banner_list.html'

    def get_queryset(self):
        # Пользователь может видеть только свои баннеры
        return BannerOrder.objects.filter(user=self.request.user)




@csrf_exempt
def submit_banner_order(request):
    print(request.POST.get('text'))
    print(request.POST.get('user'))
    print(request.user)
    print(request.FILES.get('canvas_image'))

    if request.method == 'POST':
        try:
            # Получаем данные из формы
            width = request.POST.get('width')
            height = request.POST.get('height')
            user = request.user
            text = request.POST.get('text')
            phone = request.POST.get('phone')
            bg_color = request.POST.get('bg_color')
            text_color = request.POST.get('text_color')
            grommet_type = request.POST.get('grommet_type')

            # Получаем изображение из canvas
            canvas_image = request.FILES.get('canvas_image')

            if canvas_image:
                # Здесь можно сохранить данные в базу или отправить на почту
                # Например:
                from .models import BannerOrder

                order = BannerOrder.objects.create(
                    width=width,
                    height=height,
                    text=text,
                    user=user,
                    phone=phone,
                    bg_color=bg_color,
                    text_color=text_color,
                    grommet_type=grommet_type,
                    image=canvas_image
                )

                # Или отправить уведомление на почту
                # send_mail(...)

                return JsonResponse({
                    'status': 'success',
                    'message': 'Заказ принят в обработку',
                    'order_id': order.id
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Изображение не получено'
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Неверный метод запроса'
    }, status=405)


# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt  # или используйте декоратор csrf_protect с правильной передачей токена
def upload_view(request):
    print(request)
    if request.method == 'POST':
        # Получаем обычные поля формы
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Получаем изображение из canvas
        canvas_image = request.FILES.get('canvas_image')

        if canvas_image:
            # Обрабатываем изображение
            # Пример сохранения в модель
            from .models import MyModel
            from django.core.files.base import ContentFile

            # Создаем запись
            obj = MyModel.objects.create(
                title=title,
                description=description
            )

            # Сохраняем изображение
            obj.canvas_image.save(
                f'canvas_{obj.id}.png',
                ContentFile(canvas_image.read())
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Данные успешно сохранены'
            })

    return JsonResponse({
        'status': 'error',
        'message': 'Неверный запрос'
    }, status=400)
