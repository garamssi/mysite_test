from django.shortcuts import render
from blog.models import Post, Tag

def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
        }
    )


def about_me(request):
    recent_posts = Post.objects.order_by('-pk')[:6]
    main_tag = Tag.objects.get(name='대표')
    main_posts = Post.objects.filter(tags=main_tag).order_by('-pk')
    return render(
        request,
        'single_pages/about_me.html',
        {
            'recent_posts': recent_posts,
            'main_posts': main_posts,
        }
    )
