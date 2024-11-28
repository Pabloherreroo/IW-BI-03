"""
URL configuration for skiStick project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from appSkiStick.admin import custom_admin_site
from django.urls import path, include
from django.views.i18n import set_language

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', include('appSkiStick.urls')),  # Incluye las URLs de skiapp
    path('set_language/', set_language, name='set_language'),
]

