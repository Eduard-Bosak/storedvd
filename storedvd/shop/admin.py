"""
Настройки административной панели Django для управления магазином
"""
from django.contrib import admin
from shop.models import Section,Product,Discount,Order,OrderLine

# Простая регистрация модели Section
admin.site.register(Section)
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(OrderLine)

class ProductAdmin(admin.ModelAdmin):
    """Настройки отображения товаров в админке"""
    list_display = ('title','section','image','price','data')  # Поля для отображения в списке
    list_per_page = 2  # Количество товаров на странице
    search_fields = ('title','cast')  # Поля для поиска




class DiscountAdmin(admin.ModelAdmin):
    """Настройки отображения скидок в админке"""
    list_display = ('code','value_percent')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Настройки отображения заказов в админке"""
    list_display = ('id','display_products','name','discount','phone','email','address','notice',
                      'date_order','status'
      )
    # Группировка полей в админке
    fieldsets = (
          ('Информация о заказе',{
           'fields': ['need_delivery','discount']
          }),
          ('Информация о клиенте',{
           'fields':['name','phone','email','address'],
            'description': 'Контактная информация'
          }),
          ('Доставка и оплата', {
              'fields': ['data_send', 'status']
          }),
      )

    date_hierarchy = 'date_order'  # Фильтр по дате


class OrderLineAdmin(admin.ModelAdmin):
    """Настройки отображения строк заказа в админке"""
    list_display = ('order','product','price','count')

# Регистрация моделей с кастомными админ-классами
admin.site.register(Product,ProductAdmin)
admin.site.register(Discount,DiscountAdmin)
admin.site.register(OrderLine,OrderLineAdmin)

