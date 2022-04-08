from django.contrib import admin
from app.scraper.models import ArticleHeadline, ArticleCategory, MediaSite

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
    list_display = ("name", "color")

class MediaSiteAdmin(admin.ModelAdmin):
    list_display = ("name", "human_name", "scraper", "site_url", "last_scraped")

admin.site.register(ArticleHeadline, ArticleHeadLineAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(MediaSite, MediaSiteAdmin)