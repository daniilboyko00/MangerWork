from django.db import models
from django.utils import timezone


class Offer(models.Model):
    number = models.BigIntegerField( null=False, unique=True, primary_key=True)
    product_name = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=10)
    full_cost = models.BigIntegerField()
    qntunits = models.CharField(max_length=10)
    quantity = models.FloatField()
    validity = models.DateTimeField()
    trade_category = models.CharField(max_length=255)
    country = models.CharField( max_length=255, null=True)
    status_in_trade = models.CharField(max_length=255, default=None)
    status = models.CharField(max_length=100, null=True)


    def __str__(self) -> str:
        return f'trade {self.number}'



class Bid(models.Model):

    STATUS_CHOICES = (
        ('ACTIVE','active'),
        ('INACTIVE', 'inactive')
    )

    
    TRADE_STATUS_CHOICES = (
        (1,'send_offers'),
        (2, 'close period'),
        (3,'lead_offer'),
        (4, 'result trades')
    )

    purchase_order  = models.IntegerField(blank=False, null=False, unique=True)
    application_date = models.DateTimeField(null=True)
    application_validity_period = models.DateTimeField(null=True)
    procurement_name = models.TextField( null=True)
    product_information = models.TextField( null=True)
    brand = models.CharField(max_length=255, null=True)
    producing_country = models.CharField(max_length=150, null=True)
    buyer_country = models.CharField(max_length=150, null=True)
    qntunits = models.CharField( max_length=30, null=True)
    terms_of_payment  = models.TextField( null=True)
    delivery_conditions = models.TextField( null=True)
    delivery_time = models.CharField(max_length=100, null=True)
    exposure_time = models.DateTimeField( null=True)
    application_is_bidding = models.CharField(max_length=255)
    price = models.FloatField()
    number_of_goods = models.IntegerField()
    cost = models.FloatField()
    currency = models.CharField(max_length=50)
    technical_documentation_file_name = models.CharField(max_length=100, null=True)
    application_link = models.URLField(null=True)
    scraping_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True,db_index=True, verbose_name='URL')
    comment = models.TextField(null=True, blank=True, default=None)
    tnvedcode = models.BigIntegerField( null=True)
    number_of_subcount = models.IntegerField(null=True)
    subcount_link = models.URLField( null=True)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES, default='ACTIVE')
    trade_status = models.CharField(choices=TRADE_STATUS_CHOICES, max_length=100, null=True, default=None)
    trade_status_message = models.CharField(max_length=255, null=True, default=None)
    offer = models.ManyToManyField(Offer)
    activityStatus = models.IntegerField(null=True, default=0)


class Auth_token(models.Model):
    value = models.CharField('auth-token', max_length=255)



class Notification(models.Model):
    id = models.BigIntegerField('id', primary_key=True)
    date = models.DateTimeField()
    message = models.TextField('message')
    is_read = models.BooleanField()