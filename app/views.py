from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from .models import Post, Comments, Tag, Profile, WebsiteMeta
from .forms import CommentForm, SubscribeForm
from django.contrib.auth.models import User
from django.db.models import Count


# Create your views here.
def index(request):
    top_posts = Post.objects.all().order_by("-view_count")[:3]
    recent_posts = Post.objects.all().order_by("-last_update")[:3]
    featured_post = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    website_meta = None

    if WebsiteMeta.objects.all().exists():
        website_meta = WebsiteMeta.objects.all().first()

    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful = 'Subscribed Successfully'
            subscribe_form = SubscribeForm()

    context = {
        'top_posts': top_posts,
        'recent_post': recent_posts,
        'subscribe_form': subscribe_form,
        'subscribe_successful': subscribe_successful,
        'featured_post': featured_post.first(),
        'website_meta': website_meta
    }
    return render(request, 'app/index.html', context)


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    tags = Tag.objects.all()
    top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[:3]
    recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_update')[:3]
    context = {
        'tag': tag,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'tags': tags
    }

    return render(request, 'app/tag.html', context)


def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)

    top_posts = Post.objects.filter(author=profile.user).order_by('-view_count')[:2]
    recent_posts = Post.objects.filter(author=profile.user).order_by('-last_update')[:3]
    top_authors = User.objects.annotate(number=Count('post')).order_by('number')

    context = {
        'profile': profile,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        'top_authors': top_authors
    }

    return render(request, 'app/author.html', context)


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


def search_post(request):
    search_query = request.GET.get('q') or ''
    posts = Post.objects.filter(title__icontains=search_query)

    context = {
        'posts': posts
    }
    return render(request, 'app/search.html', context)


def about(request):
    if WebsiteMeta.objects.all().exists():
        website_meta = WebsiteMeta.objects.all().first()
    context = {
        "website_meta": website_meta
    }
    return render(request, 'app/about.html', context)


def all_posts(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }

    return render(request, 'app/all_posts.html', context)