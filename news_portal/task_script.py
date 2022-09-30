import sqlite3
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_portal.settings")

import django
django.setup()

from news.models import *

# удаление записей из базы данных
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
user_frod = User.objects.create_user('Frodo')

# 2. Создать два объекта модели Author, связанные с пользователями.
auth_gend = Author.objects.create(auth_user=user_gend)
auth_arag = Author.objects.create(auth_user=user_arag)

# 3. Добавить 4 категории в модель Category
cat_magic = Category.objects.create(name = 'magic')
cat_ships = Category.objects.create(name = 'ships')
cat_arms = Category.objects.create(name = 'arms')
cat_hobbits = Category.objects.create(name = 'hobbits')

# 4. Добавить 2 статьи и 1 новость.
art_1 = Post(author=auth_gend, post_type=Post.article,
            head= 'ships arrived to Rivensdale', text='art_1 lorem ipsum '+'ipsum '*100)
art_1.save()
art_2 = Post(author=auth_gend, post_type=Post.article,
            head= 'Magic is not effective over dragons', text='art_2 lorem ipsum '+'ipsum '*100)
art_2.save()
news_1 = Post(author=auth_arag, post_type=Post.news,
            head= 'Sword is the best arm in hobbit hands', text='news_1 lorem ipsum '+'ipsum '*100)
news_1.save()

# 5. Присвоить им категории (как минимум в одной
#    статье/новости должно быть не меньше 2 категорий).
art_1.category.add(cat_magic)
art_1.category.add(cat_ships)

art_2.category.add(cat_magic)

news_1.category.add(cat_hobbits)
news_1.category.add(cat_arms)

# 6. Создать как минимум 4 комментария
#    к разным объектам модели Post (в каждом объекте
#    должен быть как минимум один комментарий).
com_1 = art_1.comment_set.create(user=user_frod, text='this is exellent')
com_2 = user_arag.comment_set.create(post=art_1, text='very usefull article')
com_3 = art_1.comment_set.create(user=user_arag, text='ships are mightly')

com_4 = art_2.comment_set.create(user=user_arag, text='big bow can damage dragon')
com_5 = art_2.comment_set.create(user=user_frod, text='dragon wish gold and gems')

com_6 = news_1.comment_set.create(user=user_frod, text='knife is better')
com_7 = news_1.comment_set.create(user=user_gend, text='hobbits can not use magic')

# 7. Применяя функции like() и dislike() к статьям/новостям и
#    комментариям, скорректировать рейтинги этих объектов.
art_1.like()
art_1.like()
art_1.like()
art_1.like()

art_2.like()
art_2.dislike()
art_2.like()
art_2.like()

news_1.dislike()
news_1.dislike()
news_1.like()
news_1.like()
news_1.like()
news_1.like()
news_1.like()

com_1.like()
com_2.like()
com_2.like()
com_3.dislike()
com_4.dislike()
com_4.dislike()
com_5.like()
com_6.like()
com_7.like()

# 8. Обновить рейтинги пользователей
for author in Author.objects.all():
    author.update_rating()
# 9. Вывести username и рейтинг лучшего пользователя
#    (применяя сортировку и возвращая поля первого объекта).
dict_1 = (Author.objects.order_by('-auth_rating')
        .values('auth_user__username','auth_rating')[0])
print(f'Best user: {dict_1["auth_user__username"]}, rating: {dict_1["auth_rating"]}\n')

# 10. Вывести дату добавления, username автора, рейтинг,
#     заголовок и превью лучшей статьи, основываясь
#     на лайках/дислайках к этой статье.
best_post_q = Post.objects.order_by('-rating')
bst_pdic = best_post_q.values('time_create',
                'author__auth_user__username','rating','head')[0]

print('Best article\n'
      f'  Create date: {bst_pdic["time_create"].date()}, '
      f'author username: {bst_pdic["author__auth_user__username"]}, '
      f'rating: {bst_pdic["rating"]}\n'
      f'  Article header: {bst_pdic["head"]}')
print(f'  Article preview: {best_post_q[0].preview()}\n')

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

print('Comments to best article')
for comm in Comment.objects.filter(post=best_post_q[0].id).values('time_create',
                'user__username', 'rating', 'text'):
    print(f'  Create date: {comm["time_create"].date()}, '
        f'username: {comm["user__username"]}, '
        f'rating: {comm["rating"]}, '
        f'Comment text: {comm["text"]}')
