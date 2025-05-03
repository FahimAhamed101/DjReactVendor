from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from userauths import views as userauths_views

urlpatterns = [
    # USER ENDPOINTS
    path("user/token/", userauths_views.MyTokenObtainPairView.as_view()),
    path("user/token/refresh/", TokenRefreshView.as_view()),
    path("user/register/", userauths_views.RegisterView.as_view()),

]