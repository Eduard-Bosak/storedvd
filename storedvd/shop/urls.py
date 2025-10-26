"""
URL-маршруты для приложения магазина
"""
# from django.conf.urls import url
from django.urls import path,re_path

from shop import views

# Список URL-шаблонов
urlpatterns= [
    path('',views.index,name='index'),  # Главная страница
    path('delivery',views.delivery,name='delivery'),  # Информация о доставке
    path('contacts',views.contacts,name='contacts'),  # Контактная информация
    re_path(r'^section/(?P<id>\d+)$',views.section,name = 'section'),  # Товары раздела
    re_path(r'^product/(?P<pk>\d+)$',views.ProductDetailView.as_view(),name = 'product'),  # Детали товара
    path('search',views.search,name='search'),  # Поиск товаров
]