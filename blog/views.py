from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Post


def post_list(request):
    # posts = get_object_or_404(Post, id=2)
    posts = Post.objects.all()
    result = [post.title for post in posts]

    return HttpResponse(result)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})