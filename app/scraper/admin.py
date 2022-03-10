from django.contrib import admin
from app.scraper.models import ArticleHeadline, ArticleCategory

# Register your models here.


class ArticleHeadLineAdmin(admin.ModelAdmin):
    # Displayed columns
    list_display = (
        "title",
        "source",
        "scraped_date",
        "url",
    )


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(ArticleHeadline, ArticleHeadLineAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
