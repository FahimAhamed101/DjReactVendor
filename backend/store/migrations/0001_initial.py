# Generated by Django 5.2 on 2025-05-03 19:27

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.FileField(blank=True, default='category.jpg', null=True, upload_to='category')),
                ('active', models.BooleanField(default=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Category',
                'ordering': ['-title'],
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('rate', models.IntegerField(default=5, help_text='Value added here are in percentage e.g 5 = 5%')),
                ('active', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Taxes',
                'ordering': ['country'],
            },
        ),
        migrations.CreateModel(
            name='CartOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('payment_status', models.CharField(choices=[('paid', 'Paid'), ('pending', 'Pending'), ('processing', 'Processing'), ('cancelled', 'Cancelled')], default='pending', max_length=100)),
                ('order_status', models.CharField(choices=[('pending', 'Pending'), ('fulfilled', 'Fulfilled'), ('cancelled', 'Cancelled')], default='pending', max_length=100)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('saved', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('stripe_session_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('paypal_session_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('oid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghi12345', length=10, max_length=10, prefix='', unique=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ManyToManyField(blank=True, to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=1000)),
                ('discount', models.IntegerField(default=1)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_by', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='CartOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('initial_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('saved', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('oid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghi12345', length=10, max_length=10, prefix='', unique=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cartorder')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
                ('coupon', models.ManyToManyField(blank=True, to='store.coupon')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.cartorder')),
                ('order_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.cartorderitem')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.FileField(blank=True, default='product.jpg', null=True, upload_to='products')),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('old_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('stock_qty', models.PositiveBigIntegerField(default=1)),
                ('in_stock', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('in_review', 'In Review'), ('published', 'Published')], default='published', max_length=100)),
                ('featured', models.BooleanField(default=False)),
                ('views', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('rating', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('pid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghi12345', length=10, max_length=10, prefix='', unique=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, default='product.jpg', null=True, upload_to='products')),
                ('active', models.BooleanField(default=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('gid', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghi12345', length=10, max_length=10, prefix='', unique=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
            options={
                'verbose_name_plural': 'Product Images',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('color_code', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='cartorderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shipping_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('service_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('tax_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('color', models.CharField(blank=True, max_length=100, null=True)),
                ('cart_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFaq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('question', models.CharField(max_length=1000)),
                ('answer', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Product FAQs',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('reply', models.TextField(blank=True, max_length=1000, null=True)),
                ('rating', models.IntegerField(choices=[(1, '1 Star'), (2, '2 Star'), (3, '3 Star'), (4, '4 Star'), (5, '5 Star')], default=None)),
                ('active', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews & Rating',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=12, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('content', models.CharField(blank=True, max_length=1000, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
