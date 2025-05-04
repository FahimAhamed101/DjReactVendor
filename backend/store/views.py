from django.shortcuts import redirect
from django.conf import settings
from django.template.loader import render_to_string

from mailersend import emails

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from userauths.models import User

from store.models import (
    Category,
    Product,
    Gallery,
    Specification,
    Size,
    Color,
    Cart,
    CartOrder,
    CartOrderItem,
    ProductFaq,
    Review,
    Wishlist,
    Notification,
    Coupon,
    Tax,
)
from store.serializers import (
    ProductSerializer,
    CategorySerializer,
    CartSerializer,
    CartOrderSerializer,
    CartOrderItemSerializer,
    CouponSerializer,
    NotificationSerializer,
    ReviewSerializer,
)

from decimal import Decimal


import traceback
import requests



# Create your views here.


def send_notification(user=None, vendor=None, order=None, order_item=None):
    Notification.objects.create(
        user=user,
        vendor=vendor,
        order=order,
        order_item=order_item,
    )


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        AllowAny,
    ]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        AllowAny,
    ]


class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_object(self):
        slug = self.kwargs["slug"]
        return Product.objects.get(slug=slug)

class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [
        AllowAny,
    ]

    def create(self, request, *args, **kwargs):
        payload = request.data

        product_id = payload["product_id"]
        user_id = payload["user_id"]
        qty = payload["qty"]
        price = payload["price"]
        shipping_amount = payload["shipping_amount"]
        country = payload["country"]
        size = payload["size"]
        color = payload["color"]
        cart_id = payload["cart_id"]

        product = Product.objects.get(id=product_id)

        # Get the size-specific price
        size_variant = Size.objects.filter(product=product, name=size).first()
        if size_variant:
            price = size_variant.price
        else:
            price = payload[
                "price"
            ]  # fallback to default price if no size variant found

        if user_id != "undefined":
            user = User.objects.get(id=user_id)
        else:
            user = None

        tax = Tax.objects.filter(country=country).first()

        if tax:
            tax_rate = tax.rate / 100
        else:
            tax_rate = 0

        cart = Cart.objects.filter(cart_id=cart_id, product=product).first()

        if cart:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.size = size
            cart.country = country
            cart.cart_id = cart_id

            service_fee_percentage = 5 / 100
            cart.service_fee = Decimal(service_fee_percentage) * cart.sub_total

            cart.total = (
                cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            )
            cart.save()

            return Response(
                {"message": "Cart updated successfully"}, status=status.HTTP_200_OK
            )
        else:
            cart = Cart()

            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.tax_fee = int(qty) * Decimal(tax_rate)
            cart.color = color
            cart.size = size
            cart.country = country
            cart.cart_id = cart_id

            service_fee_percentage = 5 / 100
            cart.service_fee = Decimal(service_fee_percentage) * cart.sub_total

            cart.total = (
                cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee
            )
            cart.save()

            return Response(
                {"message": "Cart created successfully"}, status=status.HTTP_201_CREATED
            )


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [
        AllowAny,
    ]
    queryset = Cart.objects.all()

    def get_queryset(self):
        cart_id = self.kwargs["cart_id"]
        user_id = self.kwargs.get("user_id")

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset


class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [
        AllowAny,
    ]
    lookup_field = "cart_id"

    def get_queryset(self):
        cart_id = self.kwargs["cart_id"]
        user_id = self.kwargs.get("user_id")

        if user_id is not None:
            user = User.objects.get(id=user_id)
            queryset = Cart.objects.filter(user=user, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0

        for cart_item in queryset:
            total_shipping += float(self.calculate_shipping(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_service_fee += float(self.calculate_service_fee(cart_item))
            total_sub_total += float(self.calculate_sub_total(cart_item))
            total_total += float(self.calculate_total(cart_item))

        data = {
            "shipping": total_shipping,
            "tax": total_tax,
            "service_fee": total_service_fee,
            "sub_total": total_sub_total,
            "total": total_total,
        }

        return Response(data)

    def calculate_shipping(self, cart_item):
        return cart_item.shipping_amount

    def calculate_tax(self, cart_item):
        return cart_item.tax_fee

    def calculate_service_fee(self, cart_item):
        return cart_item.service_fee

    def calculate_sub_total(self, cart_item):
        return cart_item.sub_total

    def calculate_total(self, cart_item):
        return cart_item.total


class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    lookup_field = "cart_id"

    def get_object(self):
        cart_id = self.kwargs["cart_id"]
        item_id = self.kwargs["item_id"]
        user_id = self.kwargs.get("user_id")

        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.get(id=item_id, cart_id=cart_id, user=user)
        else:
            cart = Cart.objects.get(id=item_id, cart=cart_id)

        return cart
class ReviewListAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        product_id = self.kwargs["product_id"]

        product = Product.objects.get(id=product_id)
        reviews = Review.objects.filter(product=product)

        return reviews

    def create(self, request, *args, **kwargs):
        payload = request.data

        user_id = payload["user_id"]
        product_id = payload["product_id"]
        rating = payload["rating"]
        review = payload["review"]

        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id)

        Review.objects.create(
            user=user,
            product=product,
            rating=rating,
            review=review,
        )

        return Response(
            {"message": "Review created successfully", "status": "success"},
            status=status.HTTP_200_OK,
        )

