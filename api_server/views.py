from django.shortcuts import render
from .models import Article
from .models import Citation
from .models import ArticleStatus

from rest_framework import viewsets, filters
from .serializer import ArticleSerializer, CitationSerializer
from rest_framework.response import Response

from .scholar_interface import ScholarInterface

class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def list(self, request):
        params = request.query_params.items()
        print(params)
        
        param_dict = {}
        for item in params:
            print(item)
            print(item[0])
            param_dict[item[0] ] = item[1]

        print( param_dict)
        return super().list(request)

class CitationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Citation.objects.all()
    serializer_class = CitationSerializer
    #filter_fields = ('citing', 'cited')

    def list(self, request):
        print( request.query_params.items() )
        cited =  request.query_params.get("cited")
        citing =  request.query_params.get("citing")
        
        if cited is not None:
            if citing is not None:
                filterd = CitationViewSet.queryset.filter(cited=cited, citing=citing)
            else:
                filterd = CitationViewSet.queryset.filter(cited=cited)
        else:
            if citing is not None:
                filterd = CitationViewSet.queryset.filter(citing=citing)
            else:
                filterd = CitationViewSet.queryset   

        cited_status = ArticleStatus.objects.get(article=cited)
        if filterd.count() == 0 and cited_status.citations_expansion == False:
            print(' get scholar!!!!!')
            ret = ScholarInterface().expandByArticle( cited_status.article )
            print('finished!!!')
            print(ret)
        
        serializer =  CitationViewSet.serializer_class(filterd ,many=True)

        return Response( serializer.data )

def article_list(request):
    articles = Article.objects.all()
    return render( request, 'api_server/article_list.html', {"articles": articles} )

