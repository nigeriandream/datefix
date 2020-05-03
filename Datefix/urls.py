"""Datefix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.conf.urls import handler404, handler500, handler403
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import home, about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Account.urls')),
    path('chat/', include('Chat.urls')),
    path('payment/', include('Payment.urls')),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = handler404

# handler500 = handler500

# handler403 = handler403