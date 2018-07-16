# coding: utf-8

from rest_framework import serializers

from .models import Article, ArticleStatus, Citation


class ArticleSerializer(serializers.ModelSerializer):
    read_only = True
    class Meta:
        read_only = True
        model = Article
        fields = ('cluster_id', 'title', 'author', 'url', 'year', 'num_citations', 'num_versions', 'url_citations', 'url_versions', 'excerpt')
        

class CitationSerializer(serializers.ModelSerializer):
    citing = ArticleSerializer()
    cited = ArticleSerializer()
    read_only = True
    class Meta:
        model = Citation
        fields = ('citing', 'cited')
        read_only = True
