from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from .models import Post, Category, UserCategory
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


class Search(ListView):
    queryset = Post.objects.filter(type=0)
    ordering = '-time'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class News(ListView):
    queryset = Post.objects.filter(type=0)
    ordering = '-time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Post.objects.all()
        context['amount'] = 0
        for i in a:
            if i.type == 0:
                context['amount'] += 1
        return context


class Subscribe(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'subscribe.html'
    context_object_name = 'subscribe'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        usercategory = UserCategory(
            user=self.request.user,
            category=self.get_object()
        )
        # try:
        usercategory.save()
        # messages.success(request, f'Вы успешно подписались на раздел {self.get_object().name}')
        # except:
        #     messages.error(request, f'Вы уже подписаны на раздел {self.object().name}')
        return redirect(f'/category/{self.get_object().id}/success')


class NewsDetail(DetailView):
    queryset = Post.objects.filter(type=0)
    template_name = 'new.html'
    context_object_name = 'new'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post')
    form_class = PostForm
    model = Post
    template_name = 'createnews.html'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post')
    form_class = PostForm
    model = Post
    template_name = 'createnews.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'deletenews.html'
    success_url = reverse_lazy('news_list')


class Articles(ListView):
    queryset = Post.objects.filter(type=1)
    ordering = '-time'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        a = Post.objects.all()
        context['amount'] = 0
        for i in a:
            if i.type == 1:
                context['amount'] += 1
        return context


class Article(DetailView):
    queryset = Post.objects.filter(type=1)
    template_name = 'article.html'
    context_object_name = 'article'


class ArticlesSearch(ListView):
    queryset = Post.objects.filter(type=1)
    ordering = '-time'
    template_name = 'articlessearch.html'
    context_object_name = 'search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newsapp.add_post')
    form_class = PostForm
    model = Post
    template_name = 'createarticles.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 1
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('newsapp.change_post')
    form_class = PostForm
    model = Post
    template_name = 'createarticles.html'


class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'deletearticles.html'
    success_url = reverse_lazy('articles_list')



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class Success(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'success.html'
    context_object_name = 'success'


class ClassCategory(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')
