from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from .models import Post, Category, Tag, Comment, Task
from .forms import CommentForm, TaskForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator

class PostList(ListView):
    model = Post
    ordering = '-pk'





    def get_context_data(self, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        #context['categories'] = Category.objects.all()
        #context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        #context['categories'] = Category.objects.all()
        #context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form']=CommentForm
        return context


def categories_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)


    context = {
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count(),
        'category' : category,
        'post_list' : post_list
    }

    return render(request, 'blog/post_list.html', context)


def show_tag_posts(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all(),

    context = {
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count(),
        'tag': tag,
        'post_list' : post_list
    }
    return render(request, 'blog/post_list.html', context)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title',  'content', ]#'head_image', 'file_upload', 'category', 'tags' 'hook_msg',

    template_name = "blog/post_form_update.html"

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title',  'content' ] #'head_image', 'file_upload', 'category', 'tags''hook_msg','hook_msg',

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff


    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post=post
                comment.author=request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
         raise PermissionDenied

def todo(request):
    tasks = Task.objects.all()

    form = TaskForm()

    if request.method =='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/blog/todo/')

    context = {'tasks': tasks, 'form' : form}
    return render(request, 'todolist/todolist.html', context)

def updatTask(request, pk):

    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/blog/todo/')

    context={'form':form }


    return render(request, 'todolist/update.html', context)


def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/blog/todo/')

    context = {'item': item}
    return render(request, 'todolist/delete.html')



def postpage(request):
    post_list = Post.objects.all()
    paginator = Paginator(Post.objects.all(), 2)  # 한 페이지 당 몇개 씩 보여줄 지 지정
    page = request.GET.get('page', 1)
    post1 = paginator.get_page(page)
    return render(request, "blog/post_list.html", {"post1": post1})
