from django.shortcuts import render
from news_app.models import Post
from django.utils import timezone
from datetime import timedelta
from django.views.generic import TemplateView, ListView

# Create your views here.
class HomeView(TemplateView):
    template_name = "newsportal/home.html"

    def get_context_data(selfsellf, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breaking_news"] = (
                                       Post.objects.filter(
            published_at__isnull = False, status= "active", is_breaking_news=True
        ).order_by("-published_at"))[:3]

        context["feature_post"] = (
            Post.objects.filter(published_at__isnull=False, status = "active")
            .order_by("-published_at" , "-views_count"))

        context["trending_news"] = Post.objects.filter(
            published_at__isnull=False, status ="active"
        ).order_by("published_at")[:4]

        one_week_ago = timezone.now() - timedelta(days=7)

        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull =False, status ="active", published_at__gte =one_week_ago
        ).order_by("-published_at", "-views_count")[:5]

        return context
class PostListView(ListView):
    model =Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(selfself):
        return Post.objects.filter(
            published_at__isnull = False, status ="active"
        ).order_by("-published_at")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["popular_post"] = Post.objects.filter(
            published_at__isnull = False, status ="active").order_by("-published_at")[:5]

        return context

class CategoryListView(ListView):


class ContactCreateview(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = "newsportal/contact.html"
    form_class = ContactForm
    success_yrl =  reverse_lazy ("contact")
    success_message = "Your message has been sent successfully"

    def form_invalid(self, form):
        message.error(
            selfrequest,
            "there was an error sending your message. Please check the form",

        )
        return super().form_invalid(form)







