"""
Модели данных для приложения интернет-магазина DVD
"""
from django.db import models
import datetime
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal
from django.urls import reverse

class Section(models.Model):
    """Модель раздела/категории товаров (боевики, комедии и т.д.)"""
    title = models.CharField(
        max_length = 70,
        help_text='Тут необходимо ввести название раздела',
        unique=True,
        verbose_name='Название раздела'
    )

    class Meta:
        ordering = ['id']
        verbose_name='Раздел'
        verbose_name_plural = 'Разделы'
    def get_absolute_url(self):
        return reverse('section',args=[self.id])

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель товара (DVD диска с фильмом)"""
    section = models.ForeignKey('section',on_delete=models.SET_NULL,null=True,verbose_name='Раздел')
    title = models.CharField(max_length=70,verbose_name='Названия')
    image = models.ImageField(upload_to='images',verbose_name='Изображения',blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Цена')
    year = models.IntegerField(
        validators=[MinValueValidator(1905),MaxValueValidator(datetime.date.today().year)],
        verbose_name="Год"
    )
    country = models.CharField(max_length=70,verbose_name='Страна')
    director = models.CharField(max_length=70,verbose_name='Режисер')
    play = models.IntegerField(null=True,blank=True,verbose_name='Продолжительность',help_text='В минутах',
        validators=[MinValueValidator(1)]
    )
    cast = models.TextField(verbose_name='В ролях')
    description = models.TextField(verbose_name='Описание')
    data = models.DateTimeField(auto_now_add=True,verbose_name='Дата добавления')

    class Meta:
        ordering = ['title','year']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

        def __str__(self):
            return '{0}({1})'.format(self.title,self.section.title)

class Discount(models.Model):
    """Модель скидочного купона"""
    code = models.CharField(max_length=10,verbose_name='Купон скидок')
    value = models.IntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(50)],
        verbose_name='Размер скидки',
        help_text='В процентах'
    )

    class Meta:
        ordering = ['-value']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'
    def value_percent(self):
        return str(self.value) + '%'

    def __str__(self):
        return self.code + '('+str(self.value) + '%)'

    value_percent.short_descripshion = 'Размер скидки'

class Order(models.Model):
    """Модель заказа клиента"""
    need_delivery = models.BooleanField(verbose_name='Необходимость доставки')
    discount = models.ForeignKey(Discount,verbose_name='Скидка',on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=70,verbose_name='Имя')
    phone = models.CharField(max_length=70,verbose_name='телефон')
    email = models.CharField()
    address = models.TextField(verbose_name='Адрес',blank=True)
    notice = models.CharField(max_length=150,verbose_name='Премичания к заказу',blank=True)
    date_order = models.DateTimeField(auto_now_add=True,verbose_name='Доставка заказа')
    data_send = models.DateTimeField(null=True,blank=True,verbose_name='Дата отправки')

    # Возможные статусы заказа
    STATUSES = [
        ('NEW','Новый заказ'),
        ('APR','Подтвержден'),
        ('PAY','Оплачен'),
        ('CNL','Отменен')
    ]
    status = models.CharField(choices=STATUSES,max_length=3,default='NEW',verbose_name='Статус')


    class Meta:
        ordering = ['-date_order']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def display_products(self):
        """Возвращает строку с перечислением товаров в заказе"""
        display = ''
        for order_line in self.orderline_set.all():
            display+= '{0}:{1} шт  '.format(order_line.product.title,order_line.count)

        return display
    def display_amount(self):
        """Вычисляет общую сумму заказа с учётом скидки"""
        amount = 0
        for order_line in self.orderline_set.all():
            amount += order_line.price * order_line.count
        if self.discount:
            # Применяем скидку
            amount = round(amount * Decimal(1 - self.discount.value / 100))
        return '{0} руб.'.format(amount)

    def __str__(self):
        return 'ID:' + str(self.id)

    display_products.short_description = 'Состав заказа'
    display_amount.short_description = 'Сумма'

class OrderLine (models.Model):
    """Модель строки заказа - связывает заказ с конкретными товарами"""
    order = models.ForeignKey(Order,verbose_name='Заказ',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='Товар',on_delete=models.SET_NULL,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='цена',default=0)
    count = models.IntegerField(verbose_name='Количество',validators=[MinValueValidator(1)],default=1)

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказов'

        def __str__(self):
            return 'Заказ:(ID {0}){1}:{2}шт.'.format(self.order.id,self.product.title,self.count)

