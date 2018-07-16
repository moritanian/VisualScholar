# -*- coding:utf-8 -*-


from django.core.management.base import BaseCommand

from ...models import Article
from ...scholar_interface import ScholarInterface


# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = ''

    # コマンドライン引数を指定します。(argparseモジュール https://docs.python.org/2.7/library/argparse.html)
    def add_arguments(self, parser):
        parser.add_argument('cluster_id', nargs='+')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        for cluster_id in options['cluster_id']:
            interface = ScholarInterface()
            article = interface.createBaseArticle( cluster_id ) 
            if article is not None:
                self.stdout.write(self.style.SUCCESS('Article( cluster_id =  "%s") is created!! ' % cluster_id ))

