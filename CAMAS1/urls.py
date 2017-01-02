"""CMS1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import CAMAS1.views
import university
import student


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('student.urls')),
    url(r'^cms/', include('university.urls')),

    #user authentication urls
    url(r'^users/login/$', CAMAS1.views.login),
    url(r'^users/auth/$', CAMAS1.views.auth_view),
    url(r'^users/logout/$', CAMAS1.views.logout),
    url(r'^users/loggedin/$', CAMAS1.views.loggedin),
    url(r'^users/invalid/$', CAMAS1.views.invalid_login),

    #Bolow Software urls
    url(r'^aboutus/$', university.views.aboutus),

]
