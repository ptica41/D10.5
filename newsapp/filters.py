from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateInput

class PostFilter(FilterSet):
    time = DateFilter(lookup_expr=('gt'), widget=DateInput(attrs={'type': 'date'}), label='Дата')
    class Meta:
        model = Post
        fields = {
            'head': ['icontains'],
            'category': ['exact'],
        }
