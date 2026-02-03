# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', BannerGeneratorView.as_view(), name='banner_generator'),
    path('banners/', create_banner_view, name='order_banner'),
    path('banners_list/', Banners_ListView.as_view(), name='banners_list'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)