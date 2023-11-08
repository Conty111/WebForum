# Readme file

## WebForum

### Структура проекта
```
├── static - файлы css и javascript
    ├── background.png - задний фон сайта
    └── main.css - стили для шаблонов HTML
├── templates - шаблоны html для каждой из страниц
    ├── about.html
    ├── create_article.html
    ├── home.html login.html
    ├── page_not_found.html
    ├── post_detail.html
    ├── posts.html
    ├── post_update.html
    ├── profile.html 
    ├── sign_up.html 
    ├── template.html
    └── welcome.html
├── app.py - main файл. Из него запускать приложение
├── config_extended.py - расширенная конфигурация, предоставляемая модулем flask
├── config.py - конфигурационный файл
├── forms.py - содержит классы для форм авторизации на базе FlaskForms
├── README.md - файл, который вы сейчас читаете
└── requirements.txt - все зависимости проекта
```

### Запуск веб-приложения

 1. Установить зависимости с помощью
    
        pip install -r requirements.txt

 2. Создать файл базы данных sqlite3 в папке database (находясь в директории репозитория)
 
        mkdir database
        touch data.db
    Или изменить путь к базе данных в config.py
 3. Запустить приложение из app.py. По умолчанию используется порт 5000
        
        python app.py

