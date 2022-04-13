"""varastonhallinta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.urls import path

from varastonhallintasovellus import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.EtusivuView.as_view(), name='etusivu'),
    path('kirjautuminen/', views.kirjautuminen, name='kirjautuminen'),
    path('uloskirjautuminen/', views.uloskirjautuminen, name='uloskirjautuminen'),
    path('hallinta/', views.HallintaView.as_view(), name='hallinta'),
    path('tuotehaku/', csrf_exempt(views.tuotehaku), name="tuotehaku"),
    path('lainaus/', views.lainaus, name='lainaus'),
    #path('palautus', views.palautus, name='palautus'),
    #path('tuotteiden-lisaaminen', views.lisaaminen, name='lisaaminen'),
]
