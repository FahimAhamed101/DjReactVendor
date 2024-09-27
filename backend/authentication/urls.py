from django.urls import path
from . import views

urlpatterns = [

  #----------------------------------------------- User -----------------------------------------
    path('change/password/<int:user_id>/',views.ChangePasswordView.as_view(),name="change-password"),
    path('forget/password/<int:user_id>/',views.ForgetPasswordView.as_view(),name="forget-password"),
    #----------------------------------------------- Customer --------------------------------------
    path('customer/login/', views.CustomerLoginAPIView.as_view(), name='customer-login'),
    path('customer/register/',views.CustomerRegistrationView.as_view(),name="customer-registration"),
    path('customer/profile/<int:customer_id>/',views.CustomerProfileView.as_view(),name='customer-profile'),
    path('customer/', views.GetCustomerAPIView.as_view(), name='get-customer'),
    path('customer/add/email/',views.CustomerEmailVerificationView.as_view(),name='customer-email-verification'),
    #----------------------------------------------- Seller ---------------------------------------
    path('seller/login/', views.SellerLoginAPIView.as_view(), name='seller-login'),
    path('seller/register/',views.SellerRegistrationView.as_view(),name="seller-registration"),
    path('seller/profile/<int:seller_id>/',views.SellerProfileView.as_view(),name='seller-profile'),
    path('seller/', views.GetSellerAPIView.as_view(), name='get-seller'),
    path('seller/add/email/',views.SellerEmailVerificationView.as_view(),name='seller-email-verification'),
    path('cache-display/', views.CacheDisplayView.as_view(), name='cache-display'),
]