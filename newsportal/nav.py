from newsportal.models import Category, Post, Tag


def navigation(request):
    categories = Category.objects.all()[:3]
    tags = Tag.objects.all()[:12]
    trending_posts = Post.objects.filter(published_at__isnull=False, status="active"
    ).order_by("-views_count")[:5]

    side_categories = Category.objects.all()[:6]
        

    return{
        "categories": categories,
        "tags": tags,
        "trending_posts": trending_posts,
        "side_categories": side_categories,
    }