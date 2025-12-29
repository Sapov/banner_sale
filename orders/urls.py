# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', BannerGeneratorView.as_view(), name='banner_generator'),
    path('banners/<int:banner_id>/', BannerDetailView.as_view(), name='banner_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)