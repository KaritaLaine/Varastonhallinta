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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from varastonhallintasovellus import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.EtusivuView.as_view(), name='etusivu'),
    path('rekisteroityminen/', views.RekisteroityminenView.as_view(), name='rekisteroityminen'),
    path('kirjautuminen/', views.kirjautuminen, name='kirjautuminen'),
    path('uloskirjautuminen/', views.uloskirjautuminen, name='uloskirjautuminen'),

    path('muokkaa-kayttajaa/', views.MuokkaaKayttajaaView.as_view(), name='muokkaa-kayttajaa'),
    path('vaihda-salasana/', views.VaihdaSalasanaView.as_view(), name='vaihda-salasana'),

    path('hallinta/', views.HallintaView.as_view(), name='hallinta'),
    
    path('haku/', views.haku_tulokset, name='haku'),

    path('lainaus/', views.lainaus, name='lainaus'),
    path('suorita-lainaus/<int:pk>/', views.LainaaTuoteView.as_view(), name='suorita-lainaus'),
    path('suorita-palautus/<int:pk>/', views.PalautaTuoteView.as_view(), name='suorita-palautus'),
    
    path('lisaa-tuote/', views.LisaaTuoteView.as_view(), name='lisaaminen'),
    path('muokkaa-tuotetta/<int:pk>/', views.MuokkaaTuotettaView.as_view(), name='muokkaaminen'),
    path('poista-tuote/<int:pk>/', views.PoistaTuoteView.as_view(), name='poistaminen'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
