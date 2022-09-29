import sqlite3
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_portal.settings")

import django
django.setup()

from news.models import *

con = sqlite3.connect("db.sqlite3")
with con:
    con.execute("delete from auth_user where id>1")
    con.execute("delete from news_author")
    con.execute("delete from news_category")
    con.execute("delete from news_post")
    con.execute("delete from news_comment")
    con.execute("delete from news_postcategory")
con.close()

# 1.  создать двух пользователей
user_gend = User.objects.create_user('Gendalf')
user_arag = User.objects.create_user('Aragorn')
# 2. Создать два объекта модели Author, связанные с пользователями.
auth_gend = Author.objects.create(auth_user=user_gend)
auth_arag = Author.objects.create(auth_user=user_arag)
# 3. Добавить 4 категории в модель Category