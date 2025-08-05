Flask приложение:
Состоит из двух страниц:
1. Простая форма с динасическим добавлением и удалением input полей.
2. Страница с отображением всех сабмиченных форм.

Формы сохраняются в БД PostgreSQL в поле JSONB.
данное приложение выполнено без ORM.

Для запуска на виртуальтной машине (проверялось на Ubuntu 24.04) необходимо:
1. Клонировать репозиторий в ВМ.
2. Выполнить установку необходимых пакетов python:
    
    ```pip3 install -r requirements.txt```
    
3. Установить postgreSQL:

   ```sudo apt install postgresql postgresql-contrib```

4. Запустить сервис postgreSQL

   ```sudo systemctl start postgresql.service```

5. Подключиться к CLI от имени суперпользователя 

   ```sudo -i -u postgres psql```

   Создать пользователя flaskapp ```CREATE USER flaskapp WITH PASSWORD '1234';```
   Создать БД ```CREATE DATABASE flask_db;```
   Назначить владельца для базы ```ALTER DATABASE flask_db OWNER TO flaskapp;```
6. далее при попытке подключения к БД через psycopg или через командную строку от 
имени нового пользователя может возникать ошибка с отказом в доступе.
возможный способ ее устранения - редактирование системного файла postgres, отвечающего за
способ аутентификации ```sudo nano /etc/postgresql/{version}/main/pg_hba.cong```
В нем найти строку '"local" is for Unix domain socket connections only' под этой строкой изменить
peer на md5. 
7. Еще возможное исключение может возникнуть при создании таблицы пользователем flask_app в
базе данных flask_db. (ERROR: permission denied for schema public)
Нужно подключиться к БД flask_db от имени postgres:
```sudo -i -u postgres psql -d flask_db```
``GRANT ALL ON SCHEMA public TO flaskapp;``

   БД должна работать.

8. Запуск Gunicorn:
   ```gunicorn -w 4 -b 0.0.0.0:8000 main:app```
9. Установка nginx:
   ```sudo apt install nginx```
   Создать файл /etc/nginx/sites-enabled/flaskapp
   
   содержащий:

  > server {
      listen localhost:80;

      location / {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
       }}

10. добавть файл config.py, содержаший переменные для подключения к ДБ
   Данные в этом файле должны соответствовать созданным пользователю и паролю 
   в БД. Например:
   POSTGRES_HOST = 'localhost'
   POSTGRES_USER = 'postgres'
   POSTGRES_PASSWORD = '1234'
   POSTGRES_DB_NAME = 'flask_db'
