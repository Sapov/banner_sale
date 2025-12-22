from django.shortcuts import render


def create_banner(request):
    pass


from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class BannerGeneratorView(LoginRequiredMixin, View):
    """View для генерации баннеров"""

    def get(self, request):
        """
        Отображает страницу генератора баннеров.
        """
        context = {
            'title': 'Генератор баннеров',
            'page_name': 'banner_generator',
        }

        return render(request, 'orders/banner_generator.html', context)