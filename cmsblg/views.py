from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CommentForm, CategoryForm, FactForm
from .models import Post, Category, Fact
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.name = request.user  # set the name field to the current user
                comment.save()
                return redirect('post_detail', category_slug=post.category.slug, slug=post.slug)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'cmsblg/detail.html', {'post': post, 'form': form})

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)

    return render(request, 'cmsblg/category.html', {'category': category, 'posts': posts})

def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'cmsblg/search.html', {'posts': posts, 'query': query})

def facts(request):
    faqs = Fact.objects.all()

    return render(request, 'faqs.html', {'faqs': faqs})

class CreateFact(LoginRequiredMixin, CreateView):
    model = Fact
    form_class = FactForm
    template_name = 'createcommodity.html'
    success_url = reverse_lazy('dashboard')

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'createcategory.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        slug = slugify(form.cleaned_data['title'])
        count = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{slug}-{count}"
            count += 1
        form.instance.slug = slug
        return super().form_valid(form)