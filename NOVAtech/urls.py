from django.contrib import admin
from django.urls import path, include
from nova import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('NOVA/', include('nova.urls')),
    path('', views.redirecter),
    path('<str:str>', views.redirecter),
    path('login/', views.loginredirecter),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
