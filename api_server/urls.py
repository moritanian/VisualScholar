from django.conf.urls import include, url
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'citations', views.CitationViewSet)

urlpatterns = [
      url(r'^$', views.article_list, name='article_list') 
]
urlpatterns.extend( router.urls )
