from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .models import Blog
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import PostForm
from django.urls import reverse_lazy, reverse


def home_page(request):
    # all_posts = Blog.objects.all()
    all_posts = Blog.objects.filter(status='pub').order_by('-datetime_modified')
    context = {'post_list': all_posts}
    return render(request, 'blog/blog_page.html', context)

class PostListView(generic.ListView):
    template_name = 'blog/blog_page.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return Blog.objects.filter(status='pub').order_by('-datetime_created')


def detail_page(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})

class PostDetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_new_post.html', {'form': form})


class PostCreateView(generic.CreateView):
    form_class = PostForm
    template_name = 'blog/post_new_post.html'


def edit_post(request, pk):
   post = get_object_or_404(Blog, pk=pk)
   form = PostForm(request.POST or None, instance=post)
   if form.is_valid():
       form.save()
       return redirect('home')
   return render(request, 'blog/post_new_post.html', {"form": form} )

class PostUpdateView(generic.UpdateView):
    model = Blog
    form_class = PostForm
    template_name = 'blog/post_new_post.html'



def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/delete_page.html', context={'post': post})

class DeletePostView(generic.DeleteView):
    model = Blog
    template_name = 'blog/delete_page.html'
   #success_url = reverse_lazy('home')
    def get_success_url(self):
        return reverse('home')
