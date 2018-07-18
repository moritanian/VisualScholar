import os, sys, random

from time import sleep

from .models import Article, ArticleStatus, Citation
from .scholar.scholar import SearchScholarQuery, ClusterScholarQuery, ScholarQuerier, ScholarSettings


class ScholarInterface():

    def __init__(self):
        self.querier = ScholarQuerier()
        self.settings = ScholarSettings()

    # search articles in scholar 
    def searchScholarArticles(self, options):
        query = SearchScholarQuery()
        # TODO set search conditions
        self.querier.send_query(query)
        return self.querier.articles

    # search article in scholar by cluster_id
    def searchScholarArticle(self, cluster_id):
        query = ClusterScholarQuery(cluster=cluster_id)
        self.querier.send_query(query)
        return self.querier.articles[0]

    # search articles of citations in scholar
    def searchScholarCitations(self, cluster_id, num_citations):

        articles = []

        if num_citations < 1:
            return articles

        query = ClusterScholarQuery(cluster=cluster_id, cites=cluster_id)
        
        max_page = int ( (num_citations - 1) / query.num_results) + 1
        print("cluster_id= " + cluster_id)
        print("num_citations= " + str(num_citations))
        print("num_results = " +str(  query.num_results ))
        print("max_page= " + str(max_page))
        for i in range( max_page ):
            query.set_start( i * query.num_results )
            self.querier.send_query(query)
            articles.extend( self.querier.articles )
            print("start= " + str(i * query.num_results ))
            print("num_articles= " + str(len( self.querier.articles )))
            sleep_time =  random.randrange(20)/10.0 + 1.0
            sleep(sleep_time)

        print("num_articles= " + str(len(articles)))
        
        return articles


    # expand citations tree from one article for one depth 
    def expandByArticle(self, parent_article):
        
        if parent_article is None:
            raise Exeption("ExpandByClusterId: Not found parent article.")
        
        print("num_articles= " + str(len(articles)))
        
        return articles


    # expand citations tree from one article for one depth 
    def expandByArticle(self, parent_article):
        
        if parent_article is None:
            raise Exeption("ExpandByClusterId: Not found parent article.")

        num_add = 0

        citation_article_data_list = self.searchScholarCitations( parent_article.cluster_id, parent_article.num_citations )
        
        for article_data in citation_article_data_list:
            
            if self.validateArticleData( article_data ) is False:
                continue
                
            article = Article.objects.filter(cluster_id=article_data['cluster_id'] ).first() 
            citation = Citation.objects \
                .filter(citing=article_data['cluster_id'], cited=parent_article.cluster_id) \
                .first()

            if article is None: 
                expansion_depth = parent_article.status.expansion_depth + 1
                article = self.createArticle(article_data, expansion_depth=expansion_depth)

            else:
                print("article is not none")
                parent_depth = parent_article.status.expansion_depth
                print("parent_depth = " + str(parent_depth))
                try:
                    current_depth = article.status.expansion_depth
                    print("current_depth = " + str(current_depth))
                    if parent_depth + 1 < current_depth:
                        article.status.expansion_depth = parent_depth + 1
                        article.status.save()
                except ArticleStatus.DoesNotExist:
                    article_status = ArticleStatus(article=article, expansion_depth=parent_depth+1)
                    article_status.save()
            
            if citation is not None:
                continue
            
            # create citation instance
            citation = Citation(
                citing=article,
                cited=parent_article )
            citation.save()
            
            num_add += 1

        # check expansion flag
        parent_article.status.citations_expansion = True
        parent_article.status.save()

        return num_add

    def searchArticles(self, params):
        
        article_data_list = self.searchScholarArticles( params )
        article_list= []
        
        for article_data in article_data_list:
            article = Article.objects.get(cluster_id=article_data['cluster_id'] ) 
            
            if article is not None:
                continue

            article = self.createArticle( article_data, expansion_depth=10 )
            article_list.append( article )

        return article_list

    def validateArticleData(self, article_data):

        if article_data['cluster_id'] == None or article_data['cluster_id'] == '':
            return False


        if article_data['title'] == None or article_data['title'] == '':
            return False

        if article_data['author'] == None or article_data['author'] == '':
            return False
        
        return True

    def createArticle(self, article_data, expansion_depth=10):
        article = Article(  cluster_id=article_data['cluster_id'],
                            title=article_data['title'],
                            author=article_data['author'],
                            url=article_data['url'] if article_data['url'] is not None else '',
                            year=article_data['year'] if article_data['year'] is not None else -1,
                            num_citations=article_data['num_citations'] if article_data['num_citations'] is not None else 0,
                            num_versions=article_data['num_versions'] if article_data['num_versions']  is not None else 0,
                            url_citations=article_data['url_citations'] if article_data['url_citations'] is not None else '',
                            url_versions=article_data['url_versions'] if article_data['url_versions'] is not None else "",
                            excerpt=article_data['excerpt'] if article_data['excerpt'] is not None else ''
                            )
        article.save()

        article_status = ArticleStatus(article=article, expansion_depth=expansion_depth)
        article_status.save()
        
        return article  

    def createBaseArticle(self, cluster_id):
        article_data = self.searchScholarArticle( cluster_id )
        return self.createArticle( article_data, expansion_depth=0 )

    def setBaseArticle(self, cluster_id):

        article = Article.objects.get(cluster_id=cluster_id)
        if article is None :
            raise Exeption("setBaseArticle: article is not found")
        if article.status is None:
            raise Exeption("setBaseArticle: article.status is not found")

        article.status.expansion_depth = 0
        article.status.save()


    def expandOne(self):

        result = {'success': False, 'num_add': 0, 'base_article': None}

        target = ArticleStatus.objects \
            .filter(citations_expansion=False) \
            .order_by('expansion_depth') \
            .first()

        if target is None:
            return result

        num_add = self.expandByArticle( target.article )
        result['num_add'] = num_add
        result['success'] = True
        result['base_article'] = target.article

        return result

    def testi_old(self):
        cluster_id = "14804188782990544648"
        #self.querier
        query = ClusterScholarQuery(cluster=cluster_id, cites=cluster_id)
        query.set_num_page_results(10)
        query.set_start(9)
        self.querier.send_query(query)

        print(" ------ result ----------")
        print(" article num = " + str( len(self.querier.articles) ))

        for article in self.querier.articles:
            print( article['title'])

