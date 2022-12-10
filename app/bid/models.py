from django.db import models
from users.models import CustomUser

# Create your models here.


class Bid(models.Model):

    STATUS_CHOICES = (
        ('ACTIVE','Активные'),
        ('INACTIVE', 'Неактивные')
    )

    purchase_order = models.IntegerField(verbose_name='Заявка на покупку', blank=False, null=False, unique=True)
    application_date = models.DateTimeField(verbose_name='Дата подачи заявки')
    application_validity_period = models.DateTimeField(verbose_name='Срок действия заявки')
    procurement_name = models.TextField('Наименование покупки')
    product_information = models.TextField('Информация о товаре', null=True)
    brand = models.CharField('Бренд', max_length=255, null=True)
    producing_country = models.CharField('Страна-производитель', max_length=150, null=True)
    buyer_country = models.CharField('Страна-покупатель', max_length=150, null=True)
    qntunits = models.CharField('Единицы измерения товара', max_length=30, null=True)
    terms_of_payment  = models.TextField('Условия оплаты', null=True)
    delivery_conditions = models.TextField('Условия поставки', null=True)
    delivery_time = models.CharField('Время доставки',max_length=100, null=True)
    exposure_time = models.DateTimeField('Время экспозиции')
    application_is_bidding = models.CharField('Заявка участвует в торгах', max_length=255)
    price = models.FloatField('Цена (без НДС)')
    number_of_goods = models.IntegerField('Количество товара')
    cost = models.FloatField('Стоимость (без НДС)')
    currency = models.CharField('Валюта', max_length=50)
    technical_documentation_file_name = models.CharField('Файл технической документации', max_length=100, null=True)
    application_link = models.URLField('Ссылка на заявку')
    scraping_date = models.DateTimeField('Дата последнего парсинга', auto_now_add=True)
    slug = models.SlugField(unique=True,db_index=True, verbose_name='URL')
    comment = models.TextField('Комментарий', null=True, blank=True, default=None)
    manager_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, default=None)
    tnvedcode = models.BigIntegerField('Код', null=True)
    number_of_subcount = models.IntegerField('Количество заявок на покупку', null=True)
    subcount_link = models.URLField('Заявки на покупку', null=True)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES, default='ACTIVE')


    class Meta:
        ordering = ['-application_date']


    def __str__(self):
        return  f"Заявка №{self.purchase_order}"




