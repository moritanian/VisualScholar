from django.core.management.base import BaseCommand
 
from ...scholar_interface import ScholarInterface

class Command(BaseCommand):
 
    def add_arguments(self, parser):
        #parser.add_argument('safe')
        pass
 
    def handle(self, *args, **options):
        interface = ScholarInterface()
        result = interface.expandOne()
        if result['success']:
            print("expand one depth from Article(cluster_id={0})'. {1} articles are added.".format(result['base_article'].cluster_id, result['num_add']))
