from django.shortcuts import render, get_object_or_404, redirect
from main.models import Author, Category, Post
from main.utils import update_view
from main.forums import PostForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    forums = Category.objects.all()
    context={
        "forums":forums
    }
    return render(request, 'forums.html', context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
    }
    update_view(request, post)
    return render(request, 'detail.html', context)



# def posts(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     posts=Post.objects.filter(approved=True, categories=category)
#     context={
#         posts: posts
#     }
#     return render(request, 'posts.html', context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved=True, categories=category)
    context = {
        'posts': posts,  
        'forum': category,
    }
    return render(request, 'posts.html', context)


from django.utils.text import slugify
def generate_unique_slug(title):
    slug = slugify(title)
    unique_slug = slug
    num = 1
    while Post.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{num}'
        num += 1
    return unique_slug

@login_required
def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.slug = generate_unique_slug(new_post.title)  # Generate unique slug
            new_post.save()
            return redirect("home")
        
    context = {
        "form": form,
        "title": "Create new post",
    }

    return render(request, "create_post.html", context)



