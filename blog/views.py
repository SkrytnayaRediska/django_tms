from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    posts = Post.objects.all().order_by('publish')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        page_posts = paginator.page(page)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)

    return render(request,
                  'list.html',
                  {
                      'page': page,
                      'posts': page_posts
                  })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='draft',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    return render(request, 'detail.html', {'post': post})