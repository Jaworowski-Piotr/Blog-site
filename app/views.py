from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .models import Post, Comments
from .forms import CommentForm, SubscribeForm


# Create your views here.
def index(request):
    top_posts = Post.objects.all().order_by("-view_count")[:3]
    recent_posts = Post.objects.all().order_by("-last_update")[:3]
    subscribe_form = SubscribeForm()
    context = {
        'top_posts': top_posts,
        'recent_post': recent_posts,
        'subscribe_form': subscribe_form
    }
    return render(request, 'app/index.html', context)


def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comments.objects.filter(post=post, parent=None)
    form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('comment_id'):
                parent_comment_id = request.POST.get('comment_id')
                if parent_obj := Comments.objects.get(id=parent_comment_id):
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                comment = comment_form.save(commit=False)
                post_id = request.POST.get('post_id')
                post = Post.objects.get(id=post_id)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count += 1
    post.save()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'app/post.html', context)
