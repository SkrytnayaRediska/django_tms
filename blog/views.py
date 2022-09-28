from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag


# class PostListView(ListView):
#     queryset = Post.objects.all().order_by('publish')
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'list.html'

def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = Post.objects.filter(tagged_items__tag_id__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'list.html', {'page': page,
                                         'posts': posts,
                                         'tag': tag})


def post_share_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = "TEST URL"
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comment'])
            send_mail(subject, message, '*******', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
        sent = False
    return render(request,
                  'share_post.html',
                  {
                      'post': post,
                      'form': form,
                      'sent': sent
                  })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='draft',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    return render(request,
                  'detail.html',
                  {
                      'post': post,
                      'comments': comments,
                      'comment_form': comment_form
                   }
                  )

