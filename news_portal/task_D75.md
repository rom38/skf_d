# Проект News Portal

Продолжаем работать над проектом новостного приложения. В этом модуле мы, конечно же, добавим работу с асинхронными запросами. Для успешного выполнения этого итогового задания модуля вам необходимо:

1. Установить Redis. +
2. Установить Celery. +
3. Произвести необходимые конфигурации Django для соединения всех компонент системы. +
4. Реализовать рассылку уведомлений подписчикам после создания новости. +
5. Реализовать еженедельную рассылку с последними новостями (каждый понедельник в 8:00 утра). +

6. Просмотр отдельной новости реализован по клику на идентификатор. Лучше в этом поле выводить не айди, а заголовок новости, а айди уже передавать в качестве аргумента внутри ссылки. +
7. Желательно, чтобы названия категорий были визуально отделены друг от друга. Пока названия нескольких категорий выглядят как одна. Стоит добавить пробел или использовать возможности Бутстрап для стилизации в виде кнопок или баджей
https://getbootstrap.com/docs/5.2/components/badge/#pill-badges +
8. Желательно реализовать функцию, которая предоставить пользователям права на создание постов. Это может быть кнопка "Хочу стать автором", или ссылка в профиле пользователя.
9. При создании статьи/новости автор имеет возможность создать пост от имени другого пользователя. Для учебного проекта это не страшно, но вообще так быть не должно.
10. Крайне нежелательно прописывать в файл настроек секретный ключ Джанго, а также свои данные для входа в аккаунт электронной почты. Этот файл попадает на гитхаб и виден всему миру. Используйте внешний файл для хранения ключей, паролей, данных учётных записей. +
Ознакомьтесь со статьёй https://pythobyte.com/python-dotenv-module-90588/
и не забудьте добавить файл .env в .gitgnore.
11. Если используете переменные окружения, то в проект стоит добавить файл .env.example, в котором будут обязательно перечислены все используемые в проекте переменные с пустыми значениями. Например, так:
EMAIL_HOST_USER=EMAIL_HOST_USER


https://github.com/rom38/skf_d/tree/dev_D7/news_portal

login:pass adm:adm

Celery и Redis установил, с django все работает.
В Celery сделал рассылку на электронную почту после добавления новости, и рассылку последних новостей за неделю.

Также выполнил некоторые пожелания:
1. убрал идентификаторы из перечня новостей
2. категории визуально отделил
3. добавил в .env файл секретный ключ django и адрес своей почты

   Остальные пожелания постараюсь выполнить на ноябрьских праздниках