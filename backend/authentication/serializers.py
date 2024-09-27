from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed
from ecommerce.models import Customer,Seller
from ecommerce.serializers import CustomerAddressSerializer

User = get_user_model()

#------------------------------------------------------------ User -----------------------------------------------

class CreateUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }

    def validate(self, data):
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not email:
            raise serializers.ValidationError("Email must be required")
        if not first_name:
            raise serializers.ValidationError("First name must be required")
        if not last_name:
            raise serializers.ValidationError("Last name must be required")
        if not password:
            raise serializers.ValidationError("Password must be required")
        if password != confirm_password:
            raise serializers.ValidationError("Password and Confirm_password do not match")

        return data

    def create(self, validated_data):
        email = validated_data.get("email")
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        password = validated_data.get("password")

        user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError('Email must be required')
        if not password:
            raise serializers.ValidationError('Password must be required')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, please try again')

        data['user'] = user
        return data


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","first_name","last_name"]

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email',instance.email)
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.save()
        return instance
    
class ChangedPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id","new_password","confirm_new_password"]
        extra_kwargs = {"new_password":{"read_only":True},'confirm_new_password':{'read_only':True}}

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        if new_password is None:
            raise serializers.ValidationError({"message":"New Password is required"})
        
        if confirm_new_password is None:
            raise serializers.ValidationError({"message":"Confirm New Password is required"})

        if new_password != confirm_new_password:
            raise serializers.ValidationError({"message":"New Password and Confirm New Password is not matched"})
        return data

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')

        instance.set_password(new_password)
        instance.save()
        return instance

class EmailVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email","first_name","last_name"]


#---------------------------------------------------------- Customer -----------------------------------------------


class CustomerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    customer_address = CustomerAddressSerializer(many=True,read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'mobile',"image","customer_address"]

    def get_image(self, obj):
        image = str(obj.image)
        if image.startswith('http'):
            return image
        else:
            return f"http://127.0.0.1:8000/media/{image}"


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    customer_address = CustomerAddressSerializer(many=True,read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user","mobile","image","customer_address"]
        extra_kwargs = {
            "id": {"read_only": True}
        }
    
    def get_image(self, obj):
        image = str(obj.image)
        if image.startswith('http'):
            return image
        else:
            return f"http://127.0.0.1:8000/media/{image}"


    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['user'] = instance.user
        return representation
    
class GetCustomerProfileSerializer(serializers.ModelSerializer):
    user = UserInformationSerializer(read_only=True)
    customer_address = CustomerAddressSerializer(many=True,read_only=True)

    class Meta:
        model = Customer
        fields = ["id","user","mobile","image","customer_address"]
        extra_kwargs = {
            "id":{"read_only": True}
        }         
    def update(self, instance, validated_data):
        instance.mobile = validated_data.get('mobile') or instance.mobile
        instance.image = validated_data.get('image') or instance.image

        instance.save()

        return instance
    

#---------------------------------------------------- Seller ----------------------------------------------


class SellerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'user','address','mobile',"image"]

    def get_image(self, obj):
        image = str(obj.image)
        if image.startswith('http'):
            return image
        else:
            return f"http://127.0.0.1:8000/media/{image}"


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation
    

class SellerRegistrationSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ["id", "user","mobile","image"]
        extra_kwargs = {
            "id": {"read_only": True}
        }
    
    def get_image(self, obj):
        image = str(obj.image)
        if image.startswith('http'):
            return image
        else:
            return f"http://127.0.0.1:8000/media/{image}"


    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['user'] = instance.user
        return representation

class GetSellerProfileSerializer(serializers.ModelSerializer):
    user = UserInformationSerializer(read_only=True)

    class Meta:
        model = Seller
        fields = ["id","user","mobile","image"]
        extra_kwargs = {
            "id":{"read_only": True}
        }         


    def update(self, instance, validated_data):
        instance.mobile = validated_data.get('mobile',instance.mobile)
        instance.image = validated_data.get('image',instance.image)

        instance.save()

        return instance