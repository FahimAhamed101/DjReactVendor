from django.db import models
from backend.settings import AUTH_USER_MODEL

class Seller(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    address = models.TextField(null=True,blank=True)
    mobile = models.CharField(max_length=10,null=True)
    image = models.ImageField(default='no-image.png',upload_to='seller/image')

    def __str__(self):
        return f"{self.user.email}"

class ProductCategory(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.SET_NULL,null=True,blank=True,related_name='seller_category')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    category_image = models.ImageField(upload_to='category/image',default='no-image.png')

    def __str__(self):
        return f"{self.title}"

class Customer(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10,null=True)
    image = models.ImageField(default='no-image.png',upload_to='customer/image')

    def __str__(self):
        return f"{self.user.email}"
    
class Product(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('INR', 'INR'),
    ]

    category = models.ForeignKey(ProductCategory,on_delete=models.SET_NULL,null=True,blank=True,related_name="category_product")
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True,related_name='product_customer')
    seller = models.ForeignKey(Seller,on_delete=models.SET_NULL,null=True,related_name="product_seller")
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='product/image',default='no-image.png')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    tags = models.TextField(null=True,blank=True,default='')
    price = models.FloatField(default=0,max_length=10)
    usd_price = models.FloatField(default=83,max_length=10)
    downloads = models.IntegerField(default=0,null=True,blank=True)
    product_stemp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
     
    def tags_data(self):
        if self.tags:
            tag_list = self.tags.split(",")
            return tag_list
        else:
            return []

class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="customer_address")
    address = models.TextField()
    default_address = models.BooleanField(default=False,blank=True,null=True)

    class Meta:
        verbose_name="customer address"
        verbose_name_plural="customer addresses"

    def __str__(self):
        return f"{self.address}"

class Order(models.Model):
    PENDING = 'pending'
    COMPLETED = 'completed'

    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
    ]

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name="customer_orders")
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default=PENDING)
    
    def __str__(self):
        return f"Order {self.id} - {self.get_order_status_display()}"

class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order_items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_products")
    quantity = models.IntegerField(default=1)
    price  = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    class Meta:
        verbose_name_plural="order items"
    
    def __str__(self):
        return f"{self.product.title}"
    
class ProductRating(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="ratings_customer")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_ratings")
    rating = models.IntegerField()
    review = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="product ratings"

    def __str__(self):
        return f"{self.rating}-{self.review}"

class WishList(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True,related_name="product_wishlist")
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True,related_name="customer_wishlist")

    class Meta:
        verbose_name_plural="wishlists"