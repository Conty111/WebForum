# Readme file

## Flask web-site

### Запуск веб-приложения

 1. Установить зависимости с помощью
    
        pip install -r requirements.txt

 2. Создать файл базы данных sqlite в папке database (находясь в директории репозитория)
 
        mkdir database
        touch data.db
    Или изменить путь к базе данных в config.py
 3. Запустить приложение из app.py. По умолчанию используется порт 5000
        
        python app.py

