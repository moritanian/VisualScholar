# -*- coding:utf-8 -*-


from django.core.management.base import BaseCommand

from ...models import Article
from ...scholar_interface import ScholarInterface

from datetime import datetime

# BaseCommandを継承して作成
class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = ''

    # コマンドライン引数を指定します。(argparseモジュール https://docs.python.org/2.7/library/argparse.html)
    def add_arguments(self, parser):
        pass
        #parser.add_argument('cluster_id', nargs='+')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('This is test job. time is {0}'.format( datetime.now().strftime("%Y/%m/%d %H:%M:%S") ) ) )
