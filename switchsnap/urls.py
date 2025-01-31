"""switchsnap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
#own pages
from pages.views import homepage_view, demo_view, about_view, logout, gallery_view, img_view, privacy, shutdown_notice

from django.urls import re_path


urlpatterns = [
    path('', homepage_view, name='home'),
    path('demo/', demo_view, name='demo'),
    path('demo/&n=<int:number_of_result>', demo_view),
    path('about/', about_view, name='about'),
    path('admin/', admin.site.urls),
    url(r'', include('social_django.urls', namespace='social')),
    path('logout/', logout, name='logout'),
    path('gallery/', gallery_view, name='gallery'),
    path('gallery/&n=<int:number_of_result>', gallery_view),
    path('media/<int:media_id>/', img_view),
    path('privacy', privacy),
    path('shutdown', shutdown_notice),
    ]
