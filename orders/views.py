from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import *
from .forms import BannerOrderForm



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




class BannerDetailView(LoginRequiredMixin, DetailView):
    model = Banner
    template_name = 'banner_detail.html'
    context_object_name = 'banner'

    def get_queryset(self):
        # Пользователь может видеть только свои баннеры
        return Banner.objects.filter(user=self.request.user)





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


class BannersListView(LoginRequiredMixin, ListView):
    model = BannerOrder
    template_name = 'orders/banner_list.html'

    def get_queryset(self):
        # Пользователь может видеть только свои баннеры
        return BannerOrder.objects.filter(user=self.request.user)


class BannerDeleteView(DeleteView):
    model = BannerOrder
    success_url = reverse_lazy("banners_list")


@csrf_exempt
def submit_banner_order(request):
    print(request.POST.get('text'))
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
            price_banner = request.POST.get('total_cost')

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
                    image=canvas_image,
                    price_banner=price_banner
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
