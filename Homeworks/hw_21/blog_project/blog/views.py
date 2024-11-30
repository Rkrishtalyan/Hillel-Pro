# ---- Import Statements ----
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from blog.models import Post, Category, Tag, Comment
from blog.forms import PostForm


# ---- View Functions ----

def post_list(request):
    """
    Display a list of active posts.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template for the post list.
    :rtype: HttpResponse
    """
    posts = Post.objects.filter(is_active=True)
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    """
    Display the details of a specific post and handle new comments.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param post_id: The ID of the post to retrieve.
    :type post_id: int
    :return: Rendered template for the post details.
    :rtype: HttpResponse
    """
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
    """
    Display a list of all categories.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template for the category list.
    :rtype: HttpResponse
    """
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})


def category_detail(request, category_id):
    """
    Display the details of a specific category and its posts.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param category_id: The ID of the category to retrieve.
    :type category_id: int
    :return: Rendered template for the category details.
    :rtype: HttpResponse
    """
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category, is_active=True)
    return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})


@login_required
def new_post(request):
    """
    Handle the creation of a new post by the logged-in user.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: Rendered template for the new post form or redirect after successful creation.
    :rtype: HttpResponse
    """
    category_id = request.GET.get('category')
    category = None
    if category_id:
        category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the Post instance without committing
            post = form.save(commit=False)
            post.user = request.user.userprofile
            post.save()  # Save the post to assign an ID

            # Handle dynamically created tags
            tag_string = form.cleaned_data.get('tags', '')
            tag_list = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tag.add(tag)  # Associate tags with the post

            return redirect('post_detail', post_id=post.id)
    else:
        initial_data = {'category': category} if category else {}
        form = PostForm(initial=initial_data)

    return render(request, 'blog/new_post.html', {'form': form})
