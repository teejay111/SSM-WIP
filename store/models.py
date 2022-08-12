from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Customer(models.Model):
    email = models.EmailField(
        max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)


class Product(models.Model):
    category_list = (
        ('1', 'Guitars'),
        ('2', 'Keys and Pianos'),
        ('3', 'Drums'),
        ('4', 'Amps'),
        ('5', 'Recording')
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=category_list)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    @property
    def imgURL(self):
        url = ''
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    status_list = (
        ('1', 'Confirmed By Store'),
        ('2', 'Out for Delivery'),
        ('3', 'Delivered'),
        ('4', 'Cancelled')
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True, unique=True)
    status = models.CharField(
        max_length=80, blank=True, null=True, choices=status_list)

    @property
    def get_cart_items(self):
        total = 0
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        total = 0
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(
        default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class DeliveryInfo(models.Model):
    county_list = (('1', 'Dorset'), ('2', 'East Riding of Yorkshire'), ('3', 'East Sussex'), 
    ('4', 'Essex'), ('5', 'Gloucestershire'), ('6', 'Greater London'), ('7', 'Greater Manchester'),
    ('8', 'Hampshire'), ('9', 'Herefordshire'), ('10', 'Hertfordshire'))
    city_list = (('1', 'Bournemouth'), ('2', 'Christchurch'), ('3', 'Dorchester'), ('4', 'Evershot'),
    ('5', 'Lulworth'), ('6', 'Lyme Regis'), ('7', 'Poole'), ('8', 'Purbeck'), ('9', 'Sherborne'))
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    mobile_number = models.CharField(max_length=12, null=True)
    county = models.CharField(
        max_length=200, null=True, choices=county_list)
    city = models.CharField(max_length=200, null=True, choices=city_list)
    postcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
