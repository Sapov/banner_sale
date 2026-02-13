# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
                  path('', BannerGeneratorView.as_view(), name='banner_generator'),
                  path('banners_list/', BannersListView.as_view(), name='banners_list'),
                  path('submit-banner-order/', submit_banner_order, name='submit_banner_order'),
                  path("banner_delete/<pk>", BannerDeleteView.as_view(), name="banner_delete"),

                  path("delivery", delivery, name="delivery"),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
