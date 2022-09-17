from django.urls import path
from .views import Articles, Article, ArticlesSearch, ArticlesCreate, ArticlesUpdate, ArticlesDelete


urlpatterns = [
    path('', Articles.as_view(), name='articles_list'),
    path('<int:pk>', Article.as_view(), name='article'),
    path('search/', ArticlesSearch.as_view(), name='articles_search'),
    path('create/', ArticlesCreate.as_view(), name='articles_create'),
    path('<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
    path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete')
]