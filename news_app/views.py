from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin

from news_app.forms import ContactForm, CommentForm
from news_app.models import Post, Advertisement, Category, Tag, Contact, OurTeam, Comment
from django.utils import timezone
from datetime import timedelta
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View

    # Create your views here.

class SidebarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]

        context["advertisement"] = (
            Advertisement.objects.all().order_by("-created_at").first()
        )

        return context

class HomeView(SidebarMixin, TemplateView):
    template_name = "newsportal/home.html"

    def get_context_data(selfsellf, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breaking_news"] = (
                                       Post.objects.filter(
            published_at__isnull = False, status= "active", is_breaking_news=True
        ).order_by("-published_at"))[:3]

        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )

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


class PostDetailView(SidebarMixin, FormMixin, DetailView):
    model = Post
    template_name = "newsportal/detail/detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_queryset(self):
        query = super().get_queryset()  # Post.objects.all()
        query = query.filter(published_at__isnull=False, status="active")
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # increasing the views count of currently viewed post
        current_post = self.object
        current_post.views_count += 1
        current_post.save()

        context["related_posts"] = (
            Post.objects.filter(
                published_at__isnull=False,
                status="active",
                category=self.object.category,
            )
            .exclude(id=self.object.id)
            .order_by("-published_at", "-views_count")[:2]
        )
        context["comments"] = Comment.objects.filter(
                post=self.object).order_by("-created_at")
        return context

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})



    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.user = self.request.user
        comment.save()

        messages.success(
            self.request,
            "Your comment has been added successfully."
        )

        return super().form_valid(form)
class PostByCategoryView(SidebarMixin, ListView):
    model = Post
    template_name = 'newsportal/list/list.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(
            published_at__isnull=False,
            status='active',
            category__id=self.kwargs["category_id"],
        ).order_by("-published_at")
        return query

class CategoryListView(ListView):
    model = Category
    template_name = 'newsportal/categories.html'
    context_object_name = 'categories' #categories.object.all()

# class TagListView(ListView):
#     model = Tag
#     template_name = 'newsportal/tags.html'
#     context_object_name = 'tags'

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
class ContactCreateview(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = "newsportal/contact.html"
    form_class = ContactForm
    success_yrl = reverse_lazy ("contact")
    success_message = "Your message has been sent successfully"

    def form_invalid(self, form):
        messages.error(
            self.request,
            "there was an error sending your message. Please check the form",

        )
        return super().form_invalid(form)


class AboutView(TemplateView):
    template_name = 'newsportal/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["our_teams"] = OurTeam.objects.all()
        return context


from django.core.paginator import PageNotAnInteger, Paginator
from django.db.models import Q

# | => OR
# & => and

class PostSearchView(View):
    template_name = "newsportal/list/list.html"

    def get(self, request, *args, **kwargs):
        # query=nepali search => title=nepal or content=nepal
        print(request.GET)
        query = request.GET["query"]  # nepal => NePaL

        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
            & Q(status="active")
            & Q(published_at__isnull=False)
        ).order_by(
            "-published_at"
        )  # QuerySet => ORM

        # pagination start
        page = request.GET.get("page", 1)  # 1
        paginate_by = 1
        paginator = Paginator(post_list, paginate_by)

        try:
            posts = paginator.page(page) #1
        except PageNotAnInteger:
            posts = paginator.page(1)
        # pagination end
        popular_posts = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]

        advertisement = Advertisement.objects.all().order_by("-created_at").first()

        return render(
            request,
            self.template_name,
            {
                "page_obj": posts,
                "query": query,
                "popular_posts": popular_posts,
                "advertisement": advertisement,
            },
        )


