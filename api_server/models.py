from django.db import models

class Article(models.Model):
    cluster_id = models.CharField(primary_key=True, max_length=30)
    title = models.CharField(max_length=100, blank=True, default='')
    author = models.CharField(max_length=50, blank=True, default='')
    url = models.CharField(max_length=100, blank=True, default='')
    year = models.IntegerField(db_index=True, null=True, default=-1)
    num_citations = models.IntegerField(default=0)
    num_versions = models.IntegerField(default=0)
    url_citations = models.CharField(max_length=100, blank=True, default="")
    url_versions = models.CharField(max_length=100, blank=True, default="")
    excerpt = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.cluster_id


class Citation(models.Model):

    citing = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='citing_set')
    cited = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='cited_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "citation_id({0}), cited_id({1})".format(self.citing, self.cited)
            
    @classmethod 
    def exists(cls, **kwargs):
        return Citation.__filter(**kwargs).count() > 0

    @classmethod 
    def __filter(cls, **kwargs):
        return Citation.objects.filter( **kwargs )
 
    class Meta:
        unique_together = ( ('citing', 'cited') )


class ArticleStatus(models.Model):
    
    article = models.OneToOneField(
        Article, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='status') 
    citations_expansion = models.BooleanField(default=False, db_index=True)
    importance = models.IntegerField(default=0, db_index=True)
    expansion_depth = models.IntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.article.cluster_id


