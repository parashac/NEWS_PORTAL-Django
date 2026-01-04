from django.shortcuts import render
from news_app.models import Post
from django.utils import timezone
from datetime import timedelta
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = "newsportal/home.html"

    def get_context_data(selfsellf, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breaking_news"] = (
                                       Post.objects.filter(
            published_at__isnull = False, satus= "active", is_breaking_news=True
        ).ordered_by("-published_at"))[:3]

        context["feature_post"] = (
            Post.objects.filter(published_at__isnull=False, status = "active")
            .order_by("-published_at" , "-views_count"))
        context["trending_news"] = Post.objects.filter(
            published_at__isnull=False, status ="active"
        ).order_by("publisehd_at")[:4]

        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull =False, status ="active",published_at__gte =one_week_ago
        ).order_by("-oublished_at", "-views_count")[:5]

        return context