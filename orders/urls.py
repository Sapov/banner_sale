from django.contrib import admin
from django.urls import path, include

from orders.views import create_banner, BannerGeneratorView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('banner/', create_banner ),
    path('banner-generator/', BannerGeneratorView.as_view(), name='banner_generator'),

]
