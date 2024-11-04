from django.urls import path
from userauths import views as userauths_views

from store import views as store_views


from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [


 path('user/token/', userauths_views.MyTokenOptainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),
    path('user/register/', userauths_views.RegisterView.as_view()),
    path('user/password-reset/<email>/', userauths_views.PasswordRestEmailVerify.as_view()),
    path('user/password-change/', userauths_views.PasswordChangeView.as_view()),
    path('user/profile/<user_id>/', userauths_views.ProfileView.as_view()),

        path('category/', store_views.CategoryListAPIView.as_view()),
    path('product/', store_views.ProductListAPIView.as_view()),
     path('product/<slug:slug>/', store_views.ProductDetailAPIView.as_view()),
     path('reviews/<product_id>/',store_views.ReviewListAPIView.as_view()),
    
]