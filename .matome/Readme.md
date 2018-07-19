## 環境
cat /etc/redhat-release 
CentOS Linux release 7.5.1804 (Core) 

### vim install
sudo yum install mercurial
suso yum install ncurses-devel
sudo yum install make
sudo yum install gcc

cd /usr/local/src
sudo hg clone https://bitbucket.org/vim-mirror/vim vim

sudo ./configure --with-features=huge --enable-multibyte --disable-selinux
sudo make
sudo make install

### tig install
sudo yum install -y tig

### virtualenv py env
https://qiita.com/saitou1978/items/e82421e29e118bd397cc

git clone https://github.com/yyuu/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
exec $SHELL -l

### install for python 3.6 installation problem
http://www.atmarkit.co.jp/ait/articles/1107/22/news142.html
sudo yum install zlib zlib-devel
https://github.com/pyenv/pyenv/wiki/Common-build-problems
sudo yum install zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel

### install python3.6
pyenv install 3.6.0
pyenv versions
pyenv global 3.6.0

location:
/home/dbclass/.pyenv/versions/3.6.0/bin/python

### install django
pip install django==2.0
pip install djangorestframework
pip install django-filter 
pip install django-cors-headers

### ssh 
http://www.aikawa-net.com/view/595

### node
https://qiita.com/akippiko/items/3708016fc43da088021c

### 接続設定
#### 自分ののみ
sudo firewall-cmd --zone=public --add-rich-rule='rule family="ipv4" source address="159.28.237.76/24" port port="8000" protocol="tcp" accept' --permanent
sudo firewall-cmd --reload 

sudo firewall-cmd --remove-rich-rule 'rule family="ipv4" source address="159.28.237.76/24" port port="8000" protocol="tcp" accept'
sudo firewall-cmd --reload 

#### 外部公開
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload

sudo firewall-cmd --remove-service=http --permanent
sudo firewall-cmd --reload 



#### add 
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --reload

sudo firewall-cmd --list-all
sudo firewall-cmd --list-all --permanent

#### remove
sudo firewall-cmd --zone=public --remove-port=8000/tcp
sudo firewall-cmd --remove-service=http --permanent
sudo firewall-cmd --runtime-to-permanent 
sudo firewall-cmd --reload 

sudo firewall-cmd --remove-rich-rule 'rule family="ipv4" source address="159.28.237.76/24" port port="8000" protocol="tcp" accept'

### proxy
https://qiita.com/pcnikki/items/404329f9ad9cb6e235d4
squid -z
service squid start

## Django
### commands
- server
python manage.py runserver 0:8000 &

- stop server
ps auxw | grep runserver
kill xx

- deploy model
python manage.py makemigrations api_server # migration file作成
python manage.py migrate api_server # db反映
python manage.py showmigrations   # migration file 一覧
python manage.py sqlmigrate api_server 0001_initial # migration のsql表示

- shell
python manage.py shell
from api_server.models import Article
from api_server.models import Citation


### djanhgo user
python manage.py createsuperuser


### models
#### 暗黙制約
- NOT NULL
- primary key 指定しないときidが追加される

#### scripts
rom django.contrib.auth.models import User
User.objects.all()
me = User.objects.get(username='ola')
Post.objects.create(author = me, title = 'Sample title', text = 'Test')
Post.objects.filter(author=me)

### sqlite
- open shell
sqlite3 db.sqlite3
- show tables
.tables
- show columns
.schema api_server_citation 

### model importation
python manage.py dumpdata > dump.json

python manage.py flush
python manage.py loaddata dump.json

## nextjs
Counter
http://naoya3e.hatenablog.com/entry/next_demo
React + Redux でwebAPI叩く
https://qiita.com/kazmaw/items/a2def8978127ffb11f92

(公式)　deploying a next app
https://nextjs.org/learn/basics/deploying-a-nextjs-app/deploy-with-a-custom-server

 
##  実装
### API
- citatioins
http://153.127.193.8:8000/api/citations/?cited=14804188782990544648
- article
http://153.127.193.8:8000/api/articles/1

### cron
https://torina.top/detail/223/
1分ごと
- register one article 
python manage.py test_job '1'

- expand one layer
python manage.py expand_one 

-　定義
crontab -e
- log
tail /tmp/cron.log
- error
tail /tmp/cron_or.log

### node
npm run dev
npm run build
npm run build
npm run start

ps auxw | grep npm


- killl
ps auxw | grep node

## deploy
### djungo
yum -y install mod_wsgi
https://qiita.com/slt666666/items/8b5ac6f30a8310391cda

wsgi  問題
/usr/local/src

https://www.yoheim.net/blog.php?q=20170206
./configure --with-python=/home/dbclass/.pyenv/versions/3.6.0/bin/python

#### 静的ファイル
python manage.py collectstatic

/var/www/static　へ

### apache 
sudo service httpd restart
sudo service httpd stop 


### nginx
- start
systemctl start nginx
sudo service nginx start
- stop
sudo systemctl stop nginx
- reload
systemctl reload nginx

- error log
sudo vim /var/log/nginx/error.log
- acccess log
sudo vim /var/log/nginx/access.log
- setting

vim /etc/nginx/nginx.conf

sudo vim  /etc/nginx/conf.d/api_server.conf


### gunicorn
- settng
sudo vim /etc/systemd/system/gunicorn.service

- start
sudo gunicorn visual_scholar.wsgi -b 0.0.0.0:8000

- stop
 sudo pkill gunicorn


#### gunicorn 自動起動
https://torina.top/detail/360/
sudo vim /etc/systemd/system/scholar_gunicorn.service
sudo systemctl status scholar_gunicorn
systemctl enable scholar_gunicorn
systemctl start scholar_gunicorn


### 起動まとめ
8080: node
80 : nginx
8000 : djungo


bracket 対策
printf "\e[?2004l"

## commands
http://scholar.google.com/scholar?cluster=14804188782990544648&num=1
python scholar.py -c 10 -S 2  -C 14804188782990544648  --cites 14804188782990544648


