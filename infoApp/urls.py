"""infoApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from main import views as main_views
from word import views as word_views
from rest_framework import routers
from main.views import InformationViewSet, PartyViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'information', InformationViewSet)
router.register(r'party', PartyViewSet)
router.register(r'tag', TagViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    #main
    path('', main_views.home, name='home'),
    path('party/<str:pk>/', main_views.party, name='party'),
    path('tag/<str:pk>/', main_views.tag, name='tag'),
    path('parties/', main_views.parties, name='parties'),
    path('headline/<str:pk>/', main_views.headline, name='headline'),
    path('search/', main_views.search, name='search'),
    path('party/delete/<str:pk>/', main_views.delete_party, name='delete_party'),
    path('tag/delete/<str:pk>/', main_views.delete_tag, name='delete_tag'),
    path('info/delete/<str:pk>/', main_views.delete_info, name='delete_info'),

    #word
    path('documents/',word_views.documents, name="documents"),
    path('document/<str:pk>/', word_views.document, name="document"),
    path('createDocument/', word_views.create_document, name='create_document'),

    #registration
    path('accounts/register/', main_views.registerPage, name="register"),
    path('accounts/login/', main_views.loginPage, name="login"),
    path('logout/', main_views.logoutUser, name="logout"),

    #api
    path('api/', include(router.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)