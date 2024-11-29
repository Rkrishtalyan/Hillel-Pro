from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from blog.models import Post, Category, Comment, Tag
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
    posts = Post.objects.filter(category=category, is_active=True)
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})


@login_required
def new_post(request):
    category_id = request.GET.get('category')
    category = None
    if category_id:
        category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the Post instance to get its ID
            post = form.save(commit=False)
            post.user = request.user.userprofile
            post.save()  # Save the post to assign an ID

            # Handle dynamically created tags
            tag_data = form.cleaned_data.get('tag')
            for tag in tag_data:
                # Create the tag if it doesn't exist
                tag_instance, created = Tag.objects.get_or_create(name=tag)
                post.tag.add(tag_instance)  # Add the tag to the post

            post.save()  # Save the many-to-many relationship
            return redirect('post_detail', post_id=post.id)
    else:
        # Preselect the category if provided
        initial_data = {'category': category} if category else {}
        form = PostForm(initial=initial_data)

    return render(request, 'blog/new_post.html', {'form': form})