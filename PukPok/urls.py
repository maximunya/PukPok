from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from PP import views

router = DefaultRouter()
router.register(r'user', views.UpdateUserProfileAPI, basename='update_user_info')

urlpatterns = [
	path('', include('PP.urls')),
    path('admin/', admin.site.urls),
    path('pukpok/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

