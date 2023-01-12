"""fastformule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views


handler400 = 'fastformule.views.error_400'

handler404 = 'fastformule.views.error_404'

handler500 = 'fastformule.views.error_500'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('', include('core.urls')),
    path('', include('user.urls')),
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
]
