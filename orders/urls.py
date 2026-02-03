# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
                  path('', BannerGeneratorView.as_view(), name='banner_generator'),
                  path('banners_list/', Banners_ListView.as_view(), name='banners_list'),
                  path('submit-banner-order/', submit_banner_order, name='submit_banner_order'),
                  path('upload/', upload_view, name='upload'),
                  path('up/', up, name='up'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
