from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from blog.models import Post, Category, Comment
from blog.forms import PostForm


def post_list(request):
    posts = Post.objects.filter(is_active=True)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            message = request.POST.get('message')
            Comment.objects.create(
                message=message,
                user=request.user.userprofile,
                post=post
            )
            return redirect('post_detail', post_id=post.id)
        else:
            return redirect('login')

    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})


def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = category.post_set.filter(is_active=True)
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.userprofile
            post.save()
            form.save_m2m()
            post.send_creation_email()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', {'form': form})