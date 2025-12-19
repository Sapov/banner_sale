from django.contrib import admin
from django.urls import path, include

from orders.views import create_banner

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('banner/', create_banner ),

]
