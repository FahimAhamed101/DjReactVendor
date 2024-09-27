from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import (
    CreateUserSerializer,
    LoginSerializer,
    UserInformationSerializer,
    ChangedPasswordSerializer,
    EmailVerificationSerializer,
    CustomerSerializer,
    CustomerRegistrationSerializer,
    GetCustomerProfileSerializer,
    SellerSerializer,
    SellerRegistrationSerializer,
    GetSellerProfileSerializer
)
from ecommerce.models import Customer, Seller
from .models import User




#-------------------------------------------------------- User ------------------------------------------------

class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        serializer = ChangedPasswordSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Password Updated Successfully...."}, status=status.HTTP_202_ACCEPTED)
        return Response({"error": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordView(APIView):
    def put(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        serializer = ChangedPasswordSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Password Updated Successfully...."}, status=status.HTTP_202_ACCEPTED)
        return Response({"error": str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------------------- Customer ----------------------------------------------

class CustomerRegistrationView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            mobile = request.data.get('mobile')
            if not mobile:
                return Response({"message": "Mobile number field is required"}, status=status.HTTP_400_BAD_REQUEST)
            customer = Customer.objects.create(user=user, mobile=mobile)
            customer_serializer = CustomerRegistrationSerializer(customer)
            token = RefreshToken.for_user(user)

            response_data = {
                'token': {
                    'access_token': str(token.access_token),
                    'refresh_token': str(token),
                },
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'mobile': customer_serializer.data.get('mobile')
                },
                'customer': {
                    'id': customer_serializer.data.get('id'),
                    'mobile': customer_serializer.data.get('mobile')
                }
            }
            send_notification("New Customer registered", 'notify_registration')
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']

            token = RefreshToken.for_user(user)

            try:
                customer = Customer.objects.get(user=user)
                customer_serializer = CustomerSerializer(customer)
                customer_data = customer_serializer.data
            except Customer.DoesNotExist:
                return Response({"message": "Customer is not found"})

            response_data = {
                'access_token': str(token.access_token),
                'refresh_token': str(token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'customer': customer_data
            }
            send_notification("Customer logged in", 'notify_login')
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class CustomerEmailVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email is None:
            return Response({"message": "Email is required or not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(email=email)
            serializer = EmailVerificationSerializer(user)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"data": "User does not exist with the given email"}, status=status.HTTP_404_NOT_FOUND)

class GetCustomerAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f'customer_{request.user.id}'
        customer_data = cache.get(cache_key)

        if not customer_data:
            try:
                customer = Customer.objects.get(user=request.user)
                serializer = GetCustomerProfileSerializer(customer, context={'request': request})
                customer_data = serializer.data
                cache.set(cache_key, customer_data, timeout=300)
            except Customer.DoesNotExist:
                return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(customer_data, status=status.HTTP_200_OK)

class CustomerProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        customer_id = self.kwargs['customer_id']
        cache_key = f'customer_{customer_id}'
        customer_data = cache.get(cache_key)

        if not customer_data:
            try:
                customer = Customer.objects.get(id=customer_id)
                serializer = GetCustomerProfileSerializer(customer, context={'request': request})
                customer_data = serializer.data
                cache.set(cache_key, customer_data, timeout=300)
            except Customer.DoesNotExist:
                return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"data": customer_data})

    def put(self, request, *args, **kwargs):
        customer_id = self.kwargs.get('customer_id')
        try:
            customer = Customer.objects.get(id=customer_id)
            user = customer.user

            user_serializer = UserInformationSerializer(user, data=request.data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

            customer_serializer = GetCustomerProfileSerializer(customer, data=request.data, partial=True, context={'request': request})
            if customer_serializer.is_valid(raise_exception=True):
                customer_serializer.save()

            cache_key = f'customer_{customer_id}'
            cache.delete(cache_key)

            return Response({"data": customer_serializer.data}, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

#-------------------------------------------------------- Seller ------------------------------------------------------

class SellerRegistrationView(APIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_staff = True
            user.save()

            mobile = request.data.get('mobile')
            if not mobile:
                return Response({"message": "Mobile number field is required"}, status=status.HTTP_400_BAD_REQUEST)
            seller = Seller.objects.create(user=user, mobile=mobile)
            seller_serializer = SellerRegistrationSerializer(seller)
            token = RefreshToken.for_user(user)

            response_data = {
                'token': {
                    'access_token': str(token.access_token),
                    'refresh_token': str(token),
                },
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'mobile': seller_serializer.data.get('mobile')
                },
                'seller': {
                    'id': seller_serializer.data.get('id'),
                    'mobile': seller_serializer.data.get('mobile')
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellerLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']

            token = RefreshToken.for_user(user)

            try:
                seller = Seller.objects.get(user=user)
                seller_serializer = SellerSerializer(seller)
                seller_data = seller_serializer.data
            except Seller.DoesNotExist:
                return Response({"message": "Seller is not found"})

            response_data = {
                'access_token': str(token.access_token),
                'refresh_token': str(token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'seller': seller_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class GetSellerAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            seller = Seller.objects.get(user=request.user)
            serializer = GetSellerProfileSerializer(seller, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"message": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

class SellerProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        seller_id = self.kwargs['seller_id']
        cache_key = f'seller_{seller_id}'
        seller_data = cache.get(cache_key)

        if not seller_data:
            try:
                seller = Seller.objects.get(id=seller_id)
                serializer = GetSellerProfileSerializer(seller, context={'request': request})
                seller_data = serializer.data
                cache.set(cache_key, seller_data, timeout=300)
            except Seller.DoesNotExist:
                return Response({"message": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"data": seller_data})

    def put(self, request, *args, **kwargs):
        seller_id = self.kwargs.get('seller_id')
        try:
            seller = Seller.objects.get(id=seller_id)
            user = seller.user

            user_serializer = UserInformationSerializer(user, data=request.data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

            seller_serializer = GetSellerProfileSerializer(seller, data=request.data, partial=True, context={'request': request})
            if seller_serializer.is_valid(raise_exception=True):
                seller_serializer.save()

            cache_key = f'seller_{seller_id}'
            cache.delete(cache_key)

            return Response({"data": seller_serializer.data}, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"message": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

class SellerEmailVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email is None:
            return Response({"message": "Email is required or not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(email=email, is_staff=True)
            serializer = EmailVerificationSerializer(user)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"data": "User does not exist with the given email"}, status=status.HTTP_404_NOT_FOUND)

class CacheDisplayView(APIView):
    def get(self, request, *args, **kwargs):
        cache_key = request.query_params.get('cache_key', None)
        
        if not cache_key:
            return Response({"error": "cache_key parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        cache_data = cache.get(cache_key)
        
        if cache_data is None:
            return Response({"message": "Cache not found or expired"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"cache_key": cache_key, "data": cache_data}, status=status.HTTP_200_OK)