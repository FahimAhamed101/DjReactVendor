from django.urls import path
from . import views

urlpatterns = [
    path("home/products/",views.ProductHomeView.as_view(),name='home-product'),
    path("home/categories/",views.ProductCategoryHomeView.as_view(),name='home-product-category'),
    path("home/popular/products/",views.PopularProductView.as_view(),name='popular-product'),
    path("home/popular/sellers/",views.popular_seller,name='popular-seller'),
    path("products/",views.ProductAPIView.as_view(),name="product-lc"),
    path("product/<int:pk>/",views.ProductDetailAPIView.as_view(),name="product-rud"),
    path("product/related/<int:pk>/",views.RelatedProductView.as_view(),name="related-product"),
    path("product/tag/<str:tag_name>/",views.ProductTagAPIView.as_view(),name="product-tag"),
    path("categories/",views.ProductCategoryView.as_view(),name="product-categories"),
    path("category/title/<str:title>/",views.ProductTitleDetailCategoryView.as_view(),name="product-title-detail-categories"),
    path("orders/",views.OrderAPIView.as_view(),name="order-lc"),
    path("orderitems/",views.OrderItemAPIView.as_view(),name='order-item'),
    path("order/<int:pk>/",views.OrderDetailAPIView.as_view(),name="order-l"),
    path('add-payment/', views.create_payment_intent, name='create-payment-intent'),
    path('count_product_download/<int:product_id>/',views.count_product_download,name='count-product-download'),
    path('update-order-status/<int:order_id>/',views.update_order_status, name='update-order-status'),
    path('rating/review/<int:product_id>/',views.get_all_customer_review,name="customer-review"),


    path("sellers/",views.SellerAPIView.as_view(),name="seller-lc"),
    path("seller/add/category/<int:seller_id>/",views.seller_add_new_category,name='add-product-category'),
    path("seller/add/product/<int:seller_id>/<int:category_id>/",views.seller_add_new_product,name='seller-add-product'),
    path("seller/products/<int:seller_id>/<int:product_id>/",views.seller_edit_product,name='seller-edit-product'),
    path("seller/categories/",views.SellerProductCategoryView.as_view(),name="seller-product-categories"),
    path("seller/products/<int:seller_id>/",views.get_seller_all_product,name='get-seller-product'),
    path("seller/orders/<int:seller_id>/",views.get_seller_customer_order,name="get-seller-orders"),
    path("seller/customers/<int:seller_id>/",views.get_seller_customer,name="get-seller-customers"),
    path("seller/customer/order/<int:seller_id>/<int:customer_id>/",views.get_seller_customer_orders,name="get-seller-customer-orders"),
    path("seller/customer/orders/<int:seller_id>/",views.get_seller_all_orders,name="get-seller-all-orders"),
    path("products/<int:seller_id>/",views.seller_all_products,name="seller-product-lc"),


    path("customers/",views.CustomerAPIView.as_view(),name="customer-lc"),
    path("customer/<int:pk>/",views.CustomerDetailAPIView.as_view(),name="customer-rud"),
    path("<int:customer_id>/orderitems/",views.GetCustomerOrder.as_view(),name='customer-order'),
    path('wish-list/<int:customer_id>/',views.GetProductWishList.as_view(),name="product-wishlist"),
    path('product-wishlist/<int:customer_id>/<int:product_id>/',views.AddProductInWishList.as_view(),name="add-product-wishlist"),
    path('customer-product-count/<int:customer_id>/',views.GetCustomerProductCount.as_view(),name='customer-product-count'),
    path('total-order/<int:customer_id>/',views.GetTotalOrder.as_view(),name='get-total-order'),
    path('customer/search/',views.GetSearchingProduct.as_view(),name='get-search-product'),
    path('<int:customer_id>/orderitems/<str:date>/',views.getOrderProductDetail.as_view(),name='order-detail'),
    path('customer/address/<int:customer_id>/',views.AddCustomerAddress.as_view(),name='add-address'),
    path('customer/update-address/<int:customer_id>/<int:address_id>/',views.ModifyCustomerAddress.as_view(),name='update-address'),
    path('customer/addresses/<int:customer_id>/',views.GetAllCustomerAddress.as_view(),name="get-all-address"),
    path('customer/rating/<int:customer_id>/<int:product_id>/',views.CustomerAddingRating.as_view(),name='customer-rating'),
    path('customer/orders/<int:order_id>/',views.GetAllOrderProduct.as_view(),name='get-order'),
    path('customer/orders/<int:order_id>/<int:product_id>/',views.RemoveProductFromOrder.as_view(),name='get-order-product'),

    path('reports/daily/', views.generate_monthly_report, name='generate_daily_report'),
    path('reports/monthly/', views.generate_monthly_report, name='generate_monthly_report'),
    path('reports/yearly/', views.generate_monthly_report, name='generat_yearly_report'),
    
]