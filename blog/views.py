from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post
from django.core.mail import send_mail
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.objects.all().order_by('publish')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'list.html'


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
        # TODO: email sending
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
    return render(request, 'detail.html', {'post': post})