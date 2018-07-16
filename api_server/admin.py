from django.contrib import admin

from .models import Article, Citation, ArticleStatus

admin.site.register( Article )
admin.site.register( Citation )
admin.site.register( ArticleStatus )
