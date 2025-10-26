"""
Представления (views) для приложения магазина DVD
"""
from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Section,Product
from django.views import generic
from shop.forms import SearchForm
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def index(request):
    """Главная страница - отображает список разделов и последние товары"""
    sections = Section.objects.all().order_by('title')
    products = Product.objects.all().order_by(get_order_by_product(request))[:8]
    context = {'sections': sections,'products': products}
    return render(request,'index.html',context=context)

def get_order_by_product(request):
    """
    Определяет порядок сортировки товаров на основе GET-параметров
    
    Параметры:
    - sort: поле для сортировки (price или title)
    - up: направление сортировки (0 - по убыванию, 1 - по возрастанию)
    
    Возвращает строку для метода order_by()
    """
    order_by = ''
    if request.GET.__contains__('sort') and request.GET.__contains__('up'):
        sort = request.GET['sort']
        up = request.GET['up']
        if sort == 'price' or sort == 'title':
            if up == '0':
                order_by = '-'  # Знак минус для сортировки по убыванию
            order_by += sort
    if not order_by:
        order_by = '-data'  # По умолчанию сортировка по дате добавления (новые первыми)
    return order_by

def delivery(request):
    """Страница информации о доставке"""
    return render(request, 'delivery.html')

def contacts(request):
    """Страница контактной информации"""
    return render(request, 'contacts.html')

def section(request,id):
    """Отображает товары конкретного раздела"""
    obj = Section.objects.get(pk=id)
    products = Product.objects.filter(section__exact=obj).order_by(get_order_by_product(request))
    context = {'section' : obj,'prodacts':products}
    return render(request,'section.html',context=context)

class ProductDetailView(generic.DetailView):
    """Детальное представление товара"""
    model = Product

    def get_context_data(self, **kwargs):
        """Добавляет в контекст 4 случайных товара из того же раздела"""
        context = super(ProductDetailView,self).get_context_data(**kwargs)
        context['products'] = Product.objects.\
            filter(section__exact=self.get_object().section).\
            exclude(id=self.get_object().id).\
            order_by('?')[:4]
        return context

def handler404(request,exception):
    """Обработчик ошибки 404 - страница не найдена"""
    return  render(request,'404.html',status=404)

def search(request):
    """
    Поиск товаров по запросу пользователя
    
    Осуществляет поиск по полям: название, страна, режиссёр, актёры, описание
    Результаты разбиты на страницы (по 4 товара на странице)
    """
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
       q = search_form.cleaned_data['q']
       # Поиск по нескольким полям с использованием Q-объектов
       products = Product.objects.filter(
            Q (title__icontains = q)| Q(country__icontains = q) | Q(director__icontains = q) |
           Q (cast__icontains = q) | Q(description__icontains = q)
       )
       # Пагинация результатов
       page = request.GET.get('page',1)
       paginator = Paginator(products, 4)  # 4 товара на странице
       try:
          products = paginator.page(page)
       except PageNotAnInteger:
           # Если номер страницы не является числом - показываем первую страницу
           products = paginator.page(1)
       except EmptyPage:
           # Если номер страницы больше максимального - показываем последнюю страницу
           products = paginator.page(paginator.num_pages)
       context = {'products':products,'q':q}
       return render(request,'search.html',context=context)