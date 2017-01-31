from django.conf.urls import include, url
from . import views

urlpatterns = [
               url(r'^$',views.index, name='index'),
               #student authentication urls
               url(r'^student/login/$', views.login),
               url(r'^student/auth/$', views.auth_view),
               url(r'^student/logout/$', views.logout),
               url(r'^student/loggedin/$', views.loggedin),
               url(r'^student/invalid/$', views.invalid_login),

               #student services
               #url(r'^checkmarks/$', views.checkmarks),
               url(r'^checkmarks/$', views.get_report),
               url(r'^exam_results/$', views.get_exam_results),
               #url(r'^checkbalance/$', views.checkbalance),
    ]
