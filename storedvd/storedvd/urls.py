"""
Главная конфигурация URL для проекта storedvd

Документация по URL:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Примеры:
Function views (функциональные представления)
    1. Добавьте импорт:  from my_app import views
    2. Добавьте URL в urlpatterns:  path('', views.home, name='home')
Class-based views (классовые представления)
    1. Добавьте импорт:  from other_app.views import Home
    2. Добавьте URL в urlpatterns:  path('', Home.as_view(), name='home')
Включение другого URLconf
    1. Импортируйте функцию include(): from django.urls import include, path
    2. Добавьте URL в urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # Административная панель
    path('shop/',include('shop.urls')),  # URL-ы приложения магазина
    path('',RedirectView.as_view(url='/shop/',permanent=True)),  # Редирект с корня на /shop/

]
# Настройка обслуживания статических файлов в режиме разработки
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
# Настройка обслуживания медиа-файлов (загруженные изображения)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# Обработчик ошибки 404 - страница не найдена
handler404 = 'shop.views.handler404'