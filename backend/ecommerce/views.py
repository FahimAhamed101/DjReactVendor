from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets,status
from .pagination import (
    HomeProductPagination,
    HomeCategoryProductPagination,
    PopularProductPagination
)
from django.db.models import Avg, OuterRef, Subquery
from rest_framework.decorators import api_view,permission_classes
from .models import (
    Seller,
    ProductCategory,
    Product,
    Customer,
    Order,
    OrderItems,
    CustomerAddress,
    ProductRating,
    WishList
)
from .serializers import (
    SellerSerializer,
    SellerDetailSerializer,
    ProductCategorySerializer,
    ProductTitleDetailSerializer,
    ProductSerializer,
    ProductDetailSerializer,
    CustomerSerializer,
    CustomerDetailSerializer,
    OrderSerializer,
    OrderDetailSerializer,
    OrderItemSerializer,
    CustomerAddressSerializer,
    ProductRatingSerializer,
    CustomerOrderSerializer,
    WishListSerializer,
    CustomerProductCountSerializer,
    GetTotalOrderSerializer,
    ProductInfoSerializer,
    ProductUpdateInfoSerializer,
    SellerAddNewProductSerializer,
    SellerAddProductCategorySerializer,
    getSingleProductSellerSerializer,
    getProductSellerListSerializer,
    CustomerDetailInfoSerializer,
    SellerCustomerOrderDetailSerializer,
    OrderProductItemSerializer,
)
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny

from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY
import json

class SellerAPIView(ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    pagination_class = None

class ProductCategoryView(ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class SellerProductCategoryView(ListCreateAPIView):
    pagination_class = None
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductTitleDetailCategoryView(APIView):
    def get(self,*args,**kwargs):
        title = kwargs['title']
        category_id = ProductCategory.objects.get(title=title)
        serializer = ProductTitleDetailSerializer(category_id)
        return Response(serializer.data["category_product"])
    
class RelatedProductView(APIView):
    def get(self,*args,**kwargs):
        product_id = kwargs['pk']
        product = Product.objects.get(id=product_id)
        related_product = Product.objects.filter(category=product.category).exclude(id=product_id)
        serializer = ProductSerializer(related_product,many=True)
        return Response(serializer.data)
    
class ProductTagAPIView(APIView):
    def get(self,*args,**kwargs):
        tags = kwargs['tag_name']
        product_tag = Product.objects.filter(tags__icontains=tags)
        serializer = ProductSerializer(product_tag,many=True)
        return Response(serializer.data)
    
class ProductHomeView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = HomeProductPagination

class PopularProductView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PopularProductPagination

    def get_queryset(self):
        return Product.objects.all().order_by('-downloads')

class ProductCategoryHomeView(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    pagination_class = HomeCategoryProductPagination

class ProductAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class CustomerAPIView(ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer

class OrderAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemAPIView(CreateAPIView):
    queryset = OrderItems.objects.all()
    serializer_class = OrderItemSerializer

class OrderDetailAPIView(ListCreateAPIView):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        try:
            order_id = self.kwargs.get("pk")
            order = Order.objects.get(id=order_id)
            order_items = OrderItems.objects.filter(order=order)
            return order_items
        except Order.DoesNotExist:
            return OrderItems.objects.none() 
        except ValueError:
            return OrderItems.objects.none()
        except Exception as e:
            return OrderItems.objects.none()
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
class ProductRatingView(viewsets.ModelViewSet):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer

@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = data['amount'] 
            currency = data['currency'] 
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=['card']
            )

            return JsonResponse({
                'clientSecret': intent.client_secret
            })
        except KeyError:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@api_view(['POST'])
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=404)

    payment_status = request.data.get('status')
    print("----------------------------------------",payment_status)
    if payment_status == 'succeeded':
        order.order_status = Order.COMPLETED
    else:
        order.order_status = Order.PENDING

    order.save()
    return Response({'status': 'Order status updated'}, status=200)

class GetCustomerOrder(APIView):
    def get(self,request,*args,**kwargs):
        customer_id = self.kwargs['customer_id']
        order = Order.objects.filter(customer__id=customer_id)
        order_items = OrderItems.objects.filter(order__in=order)
        serializer = CustomerOrderSerializer(order_items,many=True)
        return Response({"data":serializer.data})

@csrf_exempt
def count_product_download(request, product_id):
    if request.method == "POST":
        product = Product.objects.get(id=product_id)
        totalDownloads = product.downloads
        totalDownloads += 1
        update_result = Product.objects.filter(id=product_id).update(downloads=totalDownloads)
        data = {
            'bool':False,
            'downloads':product.downloads
        }
        if update_result:
            data = {
                'bool':True,
                'downloads':product.downloads
            }
        return JsonResponse(data) 


class GetProductWishList(APIView):
    def get(self,request,*args, **kwargs):
        customer_id = self.kwargs['customer_id']
        wishlist_data = WishList.objects.filter(customer__id=customer_id)
        serializer = WishListSerializer(wishlist_data,many=True)
        return Response({"data":serializer.data})
    
class AddProductInWishList(APIView):
    def post(self,request,*args, **kwargs):
        customer_id = self.kwargs['customer_id']
        product_id = self.kwargs['product_id']

        try:
            customer = Customer.objects.get(id=customer_id)
            product = Product.objects.get(id=product_id)
        except Customer.DoesNotExist:
            return Response({"message":"Customer Does not exist with a given key"},status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"message":"Product does not exist with a given key"},status=status.HTTP_400_BAD_REQUEST)
        
        if WishList.objects.filter(customer=customer,product=product).exists():
            return Response({"message":"Product already exists"},status=status.HTTP_400_BAD_REQUEST)
            
        wishlist_added = WishList.objects.create(customer=customer,product=product)
        if wishlist_added:
            return Response({"message":"Product added in wishlist"},status=status.HTTP_200_OK)
        return Response({"message":"product is not added in wishlist try again"},status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request,*args,**kwargs):
        customer_id = self.kwargs['customer_id']
        product_id = self.kwargs['product_id']

        try:
            customer = Customer.objects.get(id=customer_id)
            product = Product.objects.get(id=product_id)
        except Customer.DoesNotExist:
            return Response({"message":"Customer Does not exist with a given key"},status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"message":"Product does not exist with a given key"},status=status.HTTP_400_BAD_REQUEST)
        
        wish_list =  WishList.objects.filter(customer=customer,product=product)
        if wish_list.exists():
            wish_list.delete()
            return Response({"message":"Product deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"product is not exist so deletion is not possible"},status=status.HTTP_400_BAD_REQUEST)
    

class GetCustomerProductCount(APIView):
    def get(self,request,*args,**kwargs):
        customer_id = self.kwargs.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerProductCountSerializer(customer)
        return Response({"data":serializer.data})
    

class GetTotalOrder(APIView):
    def get(self,request,*args,**kwargs):
        customer_id = self.kwargs.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        order = Order.objects.filter(customer=customer)
        serializer = GetTotalOrderSerializer(order,many=True)
        return Response({"orders":serializer.data})
    
class GetSearchingProduct(APIView):
    def get(self,request,*args,**kwargs):
        data = request.query_params.get('search')
        if not data:
            return Response({"message":"Enter something for searching an product"},status=status.HTTP_404_NOT_FOUND)
        product = Product.objects.filter(title__icontains=data) or Product.objects.filter(price__icontains=data) or Product.objects.filter(usd_price__icontains=data)
        serializer = ProductInfoSerializer(product,many=True)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    

class getOrderProductDetail(APIView):
    def get(self,request,*args, **kwargs):
        customer_id = self.kwargs['customer_id']
        date = self.kwargs['date']

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"info":"customer Does not exists"},status=status.HTTP_404_NOT_FOUND)
        
        try:
            order = Order.objects.filter(customer=customer,order_time__date=date)
        except Order.DoesNotExist:
            return Response({"info":"order Does not exists"},status=status.HTTP_404_NOT_FOUND)

        try:
            orderitems = OrderItems.objects.filter(order__in=order)
            serializer = OrderProductItemSerializer(orderitems,many=True)
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        except OrderItems.DoesNotExist:
            return Response({"info":"orderitem Does not exists"},status=status.HTTP_404_NOT_FOUND)


class AddCustomerAddress(APIView):
    def post(self, request, *args, **kwargs):
        customer_id = self.kwargs['customer_id']
        serializer = CustomerAddressSerializer(data=request.data,context={'request':request,'customer_id':customer_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":serializer.data})
        
class ModifyCustomerAddress(APIView):
    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs['customer_id']
        address_id = self.kwargs['address_id']
        c_address = CustomerAddress.objects.get(id=address_id,customer__id=customer_id)
        serializer = CustomerAddressSerializer(c_address)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        customer_id = self.kwargs['customer_id']
        address_id = self.kwargs['address_id']
        c_address = CustomerAddress.objects.get(id=address_id,customer__id=customer_id)
        serializer = CustomerAddressSerializer(c_address,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"data":serializer.data},status=status.HTTP_200_OK)
        return Response({"error":"data is not validate"},status=status.HTTP_400_BAD_REQUEST)    

    def delete(self, request, *args, **kwargs):
        customer_id = self.kwargs['customer_id']
        address_id = self.kwargs['address_id']
        c_address = CustomerAddress.objects.get(id=address_id,customer__id=customer_id)
        c_address.delete()
        return Response({"data":"deleted successfully"},status=status.HTTP_204_NO_CONTENT)


class GetAllCustomerAddress(APIView):
    def get(self,request,*args, **kwargs):
        customer_id = self.kwargs['customer_id']
        address_data = CustomerAddress.objects.filter(customer__id=customer_id)
        serializer = CustomerAddressSerializer(address_data,many=True)
        return Response({"data":serializer.data})
    
@csrf_exempt
@api_view(["POST"])
def seller_add_new_category(request,seller_id):
    if request.method == "POST":
            serializer = SellerAddProductCategorySerializer(data=request.data,context={'seller_id':seller_id})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"data":serializer.data},status=status.HTTP_200_OK)
            return Response({"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
def seller_add_new_product(request,seller_id,category_id):
      if request.method == "POST":
            serializer = SellerAddNewProductSerializer(data=request.data,context={'seller_id':seller_id,'category_id':category_id})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"data":serializer.data},status=status.HTTP_200_OK)
            return Response({"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
      
@api_view(["GET"])
def get_seller_all_product(request,seller_id):
    if request.method == "GET":
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"message":"Seller not found with a given url"},status=status.HTTP_404_NOT_FOUND)
        product_serializer = getProductSellerListSerializer(seller)
        return Response({"data":{"seller":product_serializer.data}},status=status.HTTP_200_OK)
    
@api_view(["GET","PUT","DELETE"])
@csrf_exempt
def seller_edit_product(request,seller_id,product_id):
    if request.method == "GET":
        try:
            seller = Seller.objects.get(id=seller_id)
            try:
                product = Product.objects.get(id=product_id,seller=seller)
            except Product.DoesNotExist:
                return Response({"message":"Product not found with a given product id."},status=status.HTTP_404_NOT_FOUND)
        except Seller.DoesNotExist:
            return Response({"message":"Seller not found with a given seller id."},status=status.HTTP_404_NOT_FOUND)
        
        product_serializer = ProductInfoSerializer(product)
        seller_serializer = getSingleProductSellerSerializer(seller,context={'product_data':product_serializer.data})
        return Response({"data":seller_serializer.data},status=status.HTTP_200_OK)

    if request.method == "PUT":
        try:
            seller = Seller.objects.get(id=seller_id)
            try:
                product = Product.objects.get(id=product_id,seller=seller)
            except Product.DoesNotExist:
                return Response({"message":"Product not found with a given product id."},status=status.HTTP_404_NOT_FOUND)
        except Seller.DoesNotExist:
            return Response({"message":"Seller not found with a given seller id."},status=status.HTTP_404_NOT_FOUND)
        
        product_serializer = ProductUpdateInfoSerializer(product,data=request.data,partial=True)

        if product_serializer.is_valid(raise_exception=True):
            product_serializer.save()
            seller_serializer = getSingleProductSellerSerializer(seller,context={'product_data':product_serializer.data})
            return Response({"data":seller_serializer.data},status=status.HTTP_200_OK)
        return Response({"message":"Product has failed to updated"},status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "DELETE":
        try:
            seller = Seller.objects.get(id=seller_id)
            try:
                product = Product.objects.get(id=product_id,seller=seller).delete()
                return Response({"message":"Product Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
            except Product.DoesNotExist:
                return Response({"message":"Product not found with a given product id."},status=status.HTTP_404_NOT_FOUND)
        except Seller.DoesNotExist:
            return Response({"message":"Seller not found with a given seller id."},status=status.HTTP_404_NOT_FOUND)
        
@api_view(["GET"])
def get_seller_customer_order(request,seller_id):
    if request.method == "GET":
        try:
            seller = Seller.objects.get(id=seller_id)
            order = Order.objects.all()
            product = Product.objects.filter(seller=seller)
            order_item = OrderItems.objects.filter(product__in=product,order__in=order)
            serializer = SellerCustomerOrderDetailSerializer(order_item,many=True)
            return Response({"data":{"seller":serializer.data}},status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"message":"Seller Does not exists"},status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["GET"])
def get_seller_customer(request, seller_id):
    try:
        seller = Seller.objects.get(id=seller_id)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

    seller_serializer = SellerDetailSerializer(seller)

    order_items = OrderItems.objects.filter(product__seller=seller).select_related('order__customer')
    order_item_serializer = OrderItemSerializer(order_items,many=True)
    unique_customers = order_items.values('order__customer').distinct()

    customer_ids = [item['order__customer'] for item in unique_customers]
    customers = Customer.objects.filter(id__in=customer_ids)

    customer_serializer = CustomerDetailInfoSerializer(customers, many=True)

    return Response({
        "data": {
            "seller": seller_serializer.data,
            "customers": customer_serializer.data,
            "products":order_item_serializer.data,
        }
    }, status=status.HTTP_200_OK)

@api_view(["GET","DELETE"])
def get_seller_customer_orders(request,customer_id,seller_id):
    if request.method == "GET":
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"Message":"Customer is not found"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"Message":"Seller is not found"},status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.filter(customer=customer)
        order_items = OrderItems.objects.filter(order__in=order,product__seller=seller)
        order_item_serializer = SellerCustomerOrderDetailSerializer(order_items,many=True)
        return Response({"data":order_item_serializer.data},status=status.HTTP_200_OK)
    
    if request.method == "DELETE":
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"Message":"Customer is not found"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"Message":"Seller is not found"},status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.filter(customer=customer)
        order_items = OrderItems.objects.filter(order__in=order,product__seller=seller).delete()
        return Response({"data":"customer remove success fully...."},status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def get_seller_all_orders(request,seller_id):
    try:
        customer = Customer.objects.all()
    except Customer.DoesNotExist:
        return Response({"Message":"Customer is not found"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        seller = Seller.objects.get(id=seller_id)
    except Seller.DoesNotExist:
        return Response({"Message":"Seller is not found"},status=status.HTTP_400_BAD_REQUEST)
    
    order = Order.objects.filter(customer__in=customer,order_status="completed")
    order_items = OrderItems.objects.filter(order__in=order,product__seller=seller)
    order_item_serializer = SellerCustomerOrderDetailSerializer(order_items,many=True)
    return Response({"data":order_item_serializer.data},status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def popular_seller(request):
    sellers_with_ratings = Seller.objects.annotate(
        average_rating=Avg(
            Subquery(
                ProductRating.objects.filter(
                    product__seller=OuterRef('pk')
                ).values('product').annotate(
                    avg_rating=Avg('rating')
                ).values('avg_rating')
            )
        )
    ).order_by('average_rating')

    seller_serializer = SellerDetailSerializer(sellers_with_ratings, many=True)
    
    categories = ProductCategory.objects.filter(seller__in=sellers_with_ratings)
    category_serializer = ProductCategorySerializer(categories, many=True)

    return Response({
        "data": seller_serializer.data,
        "categories": category_serializer.data
    }, status=status.HTTP_200_OK)

class CustomerAddingRating(APIView):
    def get(self,request,*args, **kwargs):
        customer_id = self.kwargs['customer_id']
        product_id = self.kwargs['product_id']
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"message":"Customer is not found with a given id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message":"Product is not found with a given id"},status=status.HTTP_400_BAD_REQUEST)
        rating = ProductRating.objects.filter(customer=customer,product=product)
        rating_serializer = ProductRatingSerializer(rating,many=True)
        return Response({"data":rating_serializer.data},status=status.HTTP_200_OK)

    
    def post(self,request,*args, **kwargs):
        customer_id = self.kwargs['customer_id']
        product_id = self.kwargs['product_id']
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"message":"Customer is not found with a given id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message":"Product is not found with a given id"},status=status.HTTP_400_BAD_REQUEST)
        
        if ProductRating.objects.filter(product=product,customer=customer).exists():
            return Response({"message":"You have aleady added rating"})
        else:
            serializer = ProductRatingSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(customer=customer,product=product)
                return Response({"data":serializer.data},status=status.HTTP_201_CREATED)
            
    
@api_view(["GET"])
def get_all_customer_review(request,product_id):
    if request.method == "GET":
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message":"Product is not exists with a given id"})
        rating = ProductRating.objects.filter(product=product)
        rating_serializer = ProductRatingSerializer(rating,many=True)
        return Response({"data":rating_serializer.data},status=status.HTTP_200_OK)
    

@api_view(["GET"])
def seller_all_products(request,seller_id):
    if request.method == "GET":
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            return Response({"message":"Seller is not found with a given id"})
        product = Product.objects.filter(seller=seller)
        product_serializer = ProductSerializer(product,many=True)
        return Response({"data":product_serializer.data},status=status.HTTP_200_OK)
    

class GetAllOrderProduct(APIView):
    def get(self,request,order_id,*args, **kwargs):
        product_item = OrderItems.objects.filter(order__id=order_id)
        product_item_serializer = OrderProductItemSerializer(product_item,many=True)
        return Response({"data":product_item_serializer.data},status=status.HTTP_200_OK)
    
class RemoveProductFromOrder(APIView):
    def delete(self,request,order_id,product_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"message":"Order is not exists"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message":"Product is not exists"},status=status.HTTP_400_BAD_REQUEST)
        
        OrderItems.objects.filter(order=order,product=product).delete()
        return Response({"message":"Product is remove successfully"},status=status.HTTP_204_NO_CONTENT)
    
import csv
import datetime
from django.http import HttpResponse
from dateutil.relativedelta import relativedelta

def generate_daily_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="daily_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Product Name', 'Quantity', 'Indian Price',"American Price"])

    today = datetime.date.today()
    
    orders = Order.objects.filter(order_time__date=today)
    for order in orders:
        for item in order.order_items.all():
            writer.writerow([order.id, item.product.title, item.quantity, item.product.price,item.product.usd_price])
    return response

def generate_monthly_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="monthly_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Product Name', 'Quantity', 'Indian Price',"American Price"])

    start_date = datetime.date.today().replace(day=1)
    end_date = (start_date + relativedelta(months=1)) - datetime.timedelta(days=1)

    orders = Order.objects.filter(order_time__date__range=[start_date, end_date])
    for order in orders:
        for item in order.order_items.all(): 
            writer.writerow([order.id, item.product.title, item.quantity, item.product.price,item.product.usd_price])
    return response

def generate_yearly_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="yearly_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Product Name', 'Quantity', 'Indian Price',"American Price"])

    start_date = datetime.date.today().replace(month=1, day=1)
    end_date = datetime.date.today().replace(month=12, day=31)
    
    orders = Order.objects.filter(order_time__date__range=[start_date, end_date])
    for order in orders:
        for item in order.order_items.all():
            writer.writerow([order.id, item.product.title, item.quantity, item.product.price,item.product.usd_price])
    return response