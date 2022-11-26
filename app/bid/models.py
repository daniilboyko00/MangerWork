from django.db import models
# Create your models here.


class Bid(models.Model):
    purchase_order = models.IntegerField(verbose_name='Заявка на покупку', blank=False, null=False)
    application_date = models.DateTimeField(verbose_name='Дата подачи заявки')
    application_validity_period = models.DateTimeField(verbose_name='Срок действия заявки')
    procurement_name = models.TextField('Наименование покупки')
    product_information = models.TextField('Информация о товаре')
    brand = models.CharField('Бренд', max_length=255)
    producing_country = models.CharField('Страна-производитель', max_length=150)
    terms_of_payment  = models.TextField('Условия оплаты')
    delivery_conditions = models.TextField('Условия поставки')
    delivery_time = models.CharField('Время доставки',max_length=100)
    exposure_time = models.DateTimeField('Время экспозиции')
    application_is_bidding = models.BooleanField('Заявка участвует в торгах')
    price = models.FloatField('Цена (без НДС)')
    number_of_goods = models.IntegerField('Количество товара')
    cost = models.FloatField('Стоимость (без НДС)')
    currency = models.CharField('Валюта', max_length=50)
    technical_documentation_file_name = models.CharField('Файл технической документации', max_length=100)
    application_link = models.URLField('Ссылка на заявку')
    scraping_date = models.DateTimeField('Дата последнего парсинга', auto_now_add=True)


    class Meta:
        ordering = ['-application_date']


    def __str__(self):
        return  f"Заявка №{self.purchase_order}"




