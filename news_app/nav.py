from news_app.models import Category
def nav(request):
    categories = Category.objects.all()[:4]
    return {"categories": categories}