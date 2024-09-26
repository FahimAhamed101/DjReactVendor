from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter



route = DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('jwt/token/', TokenObtainPairView.as_view(), name="get-token"),
    path('jwt/refresh/', TokenRefreshView.as_view(), name="token-refresh"),
   
]



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)