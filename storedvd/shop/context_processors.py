"""
Контекстные процессоры для добавления общих данных во все шаблоны
"""
from shop.models import Section
from shop.forms import SearchForm

def add_default_data(request):
    """
    Добавляет в контекст всех шаблонов:
    - Список всех разделов (для меню навигации)
    - Форму поиска
    """
    sections = Section.objects.all().order_by('title')
    search_form = SearchForm()
    return {'sections': sections,'search_form':search_form}