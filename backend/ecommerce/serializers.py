from rest_framework import serializers
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

class SellerSerializer(serializers.ModelSerializer):
    product_seller = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = Seller
        fields = ["id","user","address","product_seller","mobile","image"]

    def __init__(self,*args, **kwargs):
        super(SellerSerializer,self).__init__(*args, **kwargs)
        self.Meta.depth=1

class SellerDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Seller
        fields = ["id","user","address","mobile","image","first_name"]

    def get_first_name(self,obj):
        user = obj.user
        return user.first_name


class ProductSerializer(serializers.ModelSerializer):
    product_ratings = serializers.StringRelatedField(many=True,read_only=True)
    order_products = serializers.StringRelatedField(many=True,read_only=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id","category","image","seller","customer","title","description","downloads","tags_data","price","usd_price","product_stemp","product_ratings","order_products"]

    def get_image(self, obj):
        image = str(obj.image)
        if image.startswith('http'):
            return image
        else:
            return f"http://127.0.0.1:8000/media/{image}"

    def __init__(self,*args,**kwargs):  
        super(ProductSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth=1

class ProductCategorySerializer(serializers.ModelSerializer):
    category_product = serializers.StringRelatedField(many=True,read_only=True)
    category_image = serializers.SerializerMethodField()
    class Meta:
        model = ProductCategory
        fields = ["id","title","description","category_image","category_product"]

    def get_category_image(self,obj):
        image = str(obj.category_image)
        if image.startswith('http'):
            return image
        else:
            return f"http://127.0.0.1:8000/media/{image}"

    def __init__(self,*args,**kwargs):
        super(ProductCategorySerializer,self).__init__(*args, **kwargs)
        self.Meta.depth=1

class ProductInfoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id","category","title","description","tags","image","price","usd_price","product_stemp"]
        depth = 1

    def get_image(self,obj):
        if str(obj.image).startswith('http'):
            return obj
        else:
            return f"http://127.0.0.1:8000/media/{obj.image}"
   
    
class ProductUpdateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","category","title","description","tags","image","price","usd_price","product_stemp"]
        depth = 1

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.image = validated_data.get('image',instance.image)
        instance.price = validated_data.get('price',instance.price)
        instance.usd_price = validated_data.get('usd_price',instance.usd_price)
        instance.tags = validated_data.get('tags',instance.tags)
        instance.save()
        return instance

class ProductTitleDetailSerializer(serializers.ModelSerializer):
    category_product = ProductSerializer(many=True,read_only=True)
    class Meta:
        model = ProductCategory
        fields = ["id","title","description","category_image","category_product"]

    def __init__(self,*args,**kwargs):
        super(ProductTitleDetailSerializer,self).__init__(*args, **kwargs)
        self.Meta.depth=1

class ProductDetailSerializer(serializers.ModelSerializer):
    product_ratings = serializers.StringRelatedField(many=True,read_only=True)
    order_products = serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model = Product
        fields = ["id","category","seller","customer","title","description","customer","price","usd_price","image","downloads","tags_data","product_ratings","order_products","product_stemp"]

    def __init__(self,*args,**kwargs):
        super(ProductDetailSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth=1


class OrderSerializer(serializers.ModelSerializer):
    order_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z',read_only=True) 
    class Meta:
        model = Order
        fields = ["id", "customer", "order_time","order_status"]
        extra_kwargs = {'order_time' : {'read_only':True},'id': {'read_only':True}}

    def create(self, validated_data):
        customer = validated_data.pop('customer', None)
        if customer:
            order = Order.objects.create(customer=customer, **validated_data)
            return order
        else:
            raise serializers.ValidationError("Customer data is required for creating an order")

    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.save()
        return instance
    
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ["id","order","product"]

    def __init__(self,*args,**kwargs):
        super(OrderDetailSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth=1



class CustomerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","title","price","usd_price","product_stemp"]
    
class CustomerOrderSerializer(serializers.ModelSerializer):
    product = ProductInfoSerializer()
    class Meta:
        model = OrderItems
        fields = ["id","order","product"]

    def __init__(self, instance=None, data=..., **kwargs):
        super(CustomerOrderSerializer,self).__init__(instance, data, **kwargs)
        self.Meta.depth=1

    
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    product_title = serializers.SerializerMethodField(read_only=True)
    seller = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderItems
        fields = ['order', 'product', 'quantity','seller','price','product_title']
        extra_kwargs = {
            'order': {'required': True},
        }
        depth = 1

    def get_product_title(self,obj):
        product_title = obj.product.title
        return product_title
    
    def get_seller(self,obj):
        seller = obj.product.seller
        return seller.id
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        return representation

class OrderProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['order', 'product', 'quantity', 'price']
        extra_kwargs = {
            'order': {'required': True},
        }

    def __init__(self, instance=None, data=..., **kwargs):
        super(OrderProductItemSerializer,self).__init__(instance, data, **kwargs)
        self.Meta.depth=1

class ProductRatingSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ProductRating
        fields = ["id","customer","product","rating","review","add_time","first_name"]
        extra_kwargs = {"add_time":{"read_only":True},"id":{"read_only":True}}

    def __init__(self,*args,**kwargs):
        super(ProductRatingSerializer,self).__init__(*args, **kwargs)
        self.Meta.depth=1

    def get_first_name(self,obj):
        user = obj.customer.user
        return user.first_name.capitalize()

    def validate(self, data):
        rating = data.get('rating')

        if not rating:
            raise serializers.ValidationError("Rating must be required")
        return data
    

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ["id","product","customer"]

    def __init__(self, instance=None, data=..., **kwargs):
        super(WishListSerializer,self).__init__(instance, data, **kwargs)
        self.Meta.depth=1
    
class GetTotalOrderSerializer(serializers.ModelSerializer):
    order_time = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z',read_only=True)
    class Meta:
        model = Order
        fields = ["id","customer","order_time","order_status"]
        extra_kwargs = {'order_time' : {'read_only':True}}

class CustomerProductCountSerializer(serializers.ModelSerializer):
    customer_wishlist = WishListSerializer(many=True,read_only=True)
    order_lists = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = ['id',"user","customer_wishlist","order_lists","image"]

    def get_order_lists(self,obj):
        order = Order.objects.filter(customer=obj)
        serializers = GetTotalOrderSerializer(order,many=True)
        return serializers.data
    

class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ["id","customer","address","default_address"]

    def __init__(self,*args, **kwargs):
        super(CustomerAddressSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth=1

class CustomerSerializer(serializers.ModelSerializer):
    customer_orders = OrderSerializer(many=True,read_only=True)
    customer_address = CustomerAddressSerializer(many=True,read_only=True)
    ratings_customer = serializers.StringRelatedField(many=True,read_only=True)
    product_customer = CustomerProductSerializer(many=True,read_only=True)
    customer_wishlist = WishListSerializer(many=True,read_only=True)

    class Meta:
        model = Customer
        fields = ["id","user","mobile","image","customer_orders","customer_address","product_customer","ratings_customer","customer_wishlist"]

    def __init__(self,*args,**kwargs):
        super(CustomerSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth=1

    def validate_mobile(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Mobile number must be exactly 10 digits.")
        return value

class CustomerDetailSerializer(serializers.ModelSerializer):
    customer_orders = OrderSerializer(many=True,read_only=True)        
    customer_address = CustomerAddressSerializer(many=True,read_only=True)
    ratings_customer = serializers.StringRelatedField(many=True,read_only=True)
    product_customer = CustomerProductSerializer(many=True,read_only=True)
    customer_wishlist = WishListSerializer(many=True,read_only=True)

    class Meta:
        model = Customer
        fields = ["id","user","mobile","customer_orders","image","product_customer","customer_address","ratings_customer","customer_wishlist"]

    def __init__(self,*args,**kwargs):
        super(CustomerDetailSerializer,self).__init__(*args,**kwargs)
        self.Meta.depth=1

    def validate_mobile(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Mobile number must be exactly 10 digits.")
        return value
    
class CustomerAddressDetailSerailizer(serializers.ModelSerializer):
    customer_address = CustomerAddressSerializer(many=True,read_only=True)
    
    class Meta:
        model = Customer
        fields = ["id","user","mobile","image","customer_address"]


    def validate(self,data):
        address = data.get('address')
        if not address:
            raise serializers.ValidationError({"message":"address_field must be required"})
        return data
    
    def create(self, validated_data):
        customer_id = self.context.get('customer_id')
        customer = Customer.objects.get(id=customer_id)
        address = validated_data.get('address')
        default_address = validated_data.get('default_address')
        return CustomerAddress.objects.create(customer=customer,address=address,default_address=default_address)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.default_address = validated_data.get('default_address',instance.default_address)
        instance.save()
        return instance
    
class SellerAddProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id","seller","title","description","category_image"]

    def validate(self, data):
        title = data.get('title')
        if not title:
            raise serializers.ValidationError("Category title is required")
        return data

    def create(self, validated_data):
        seller_id = self.context.get('seller_id')

        seller = Seller.objects.get(id=seller_id)

        if not seller:
            raise serializers.ValidationError("Seller is not Found")

        return ProductCategory.objects.create(seller=seller,**validated_data)
    

class SellerAddNewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","title","description","image","tags","currency","price","usd_price","product_stemp"]

    def create(self, validated_data):
        seller_id = self.context.get('seller_id')
        seller = Seller.objects.get(id=seller_id)
        category_id = self.context.get('category_id')
        category = ProductCategory.objects.get(id=category_id)
   
        currency = validated_data.get('currency')
        price = validated_data.get('price')
        usd_price = validated_data.get('usd_price')
        tags = validated_data.get('tags')
        title = validated_data.get('title')
        description = validated_data.get('description')
        image = validated_data.get('image')

        if not title:
            raise serializers.ValidationError("Title is required for adding product")

        if currency == 'INR':
            usd_price = round(price / 83,2)
        if currency == "USD":
            price = int(usd_price * 83)

        if not seller:
            raise serializers.ValidationError("Seller is not Found")
        if not category:
            raise serializers.ValidationError("Catogory is not Found")
        return Product.objects.create(seller=seller,category=category,price=price,usd_price=usd_price,tags=tags,title=title,description=description,image=image)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = ProductCategorySerializer(instance.category).data
        representation['seller'] = SellerDetailSerializer(instance.seller).data
        return representation
    

class getProductSellerListSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Seller
        fields = ["id","user","address","mobile","image","products"]

    def get_image(self,obj):
        if str(obj.image).startswith('http'):
            return obj.image
        else:
            return f"http://127.0.0.1:8000/media/{obj.image}"

    def get_products(self,obj):
        product = Product.objects.filter(seller=obj)
        product_serializer = ProductInfoSerializer(product,many=True)
        return product_serializer.data
    
class getSellerCustomerOrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Seller
        fields = ["id","user","address","mobile","image","products"]

    def get_image(self,obj):
        if str(obj.image).startswith('http'):
            return obj.image
        else:
            return f"http://127.0.0.1:8000/media/{obj.image}"

    def get_products(self,obj):     
        product = Product.objects.filter(seller=obj)
        product_serializer = ProductInfoSerializer(product,many=True)
        return product_serializer.data
    
class getSingleProductSellerSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Seller
        fields = ["id","user","address","mobile","image","product"]

    def get_image(self,obj):
        if str(obj.image).startswith('http'):
            return obj.image
        else:
            return f"http://127.0.0.1:8000/media/{obj.image}"

    def get_product(self,obj):     
        product_data = self.context.get('product_data')
        return product_data
    
class CustomerDetailInfoSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField(read_only=True)
    date_joined = serializers.SerializerMethodField(read_only=True)
    customer_address = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id","user","email","mobile","image","date_joined","customer_address"]

    def get_email(self,obj):
        email = obj.user.email
        return email
    
    def get_date_joined(self,obj):
        date_joined = obj.user.date_joined
        return date_joined
    
    def get_customer_address(self, obj):
        get_addresses = obj.customer_address.filter(default_address=True)
        serializer = CustomerAddressSerializer(get_addresses, many=True)
        return serializer.data
    
class SellerCustomerOrderDetailSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    class Meta:
        model = OrderItems
        fields = ["id","order","product"]
        depth = 2