## Быстрый старт


Скачать проект.
```
git init
git clone https://github.com/romashovdmitry/Backend-TTC
```
Сделать вииртуальное окружениие
```
python -m venv .myenv
.\.myenv\Scripts\activate.bat  
pip install -r requirements.txt
```

Запуститиь миграции, запустить проект.
```
python app/manage.py makemigrations
python app/manage.py migrate
python app/manage.py runserver
```

# Swagger UI

Link to [Swagger UI](http://127.0.0.1:8000/api/docs/)

# Фейковые данные

Есть команда для создания фейковых данных. А именно, создаёт
- игроков
- клуб
- присваивает клуб одному из пользователей (делает игрока админом клуба)
- создаёт турнир (без распределениия игроков по группам)

В дальнейшем по мере движения Вадима, буду добавлять такие фейковые данные для его работы. 

Команда для создания этих фейковых данных: 
```
python app/manage.py create_start_environment
```
