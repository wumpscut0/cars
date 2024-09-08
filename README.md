# Cars

## Описание:
Простое веб-приложение с CRUD операциями над объявлениями с авто

## Что реализовано:
- Views c CRUD по автомобилям и с CR по комментариям.
- REST API предоставляющий управление над автомобилями(CRUD) и комментариями(CR)
- Верстка с применением bootstrap
- Логика регистрации, аутентификации и авторизации
- Умное автодополнение с применением JS, выпадающий список марок и выпадающий список моделей фильтруется согласно введённой марке
- Доступ к моделям автомобилей и комментариев в административной панели

## Технологии
- Python
- Django
- DRF
- SQLite
- HTML/CSS/JS

## Руководство по запуску
### Docker
1. Убедитесь, что в системе установлены (Версии могут отличаться):
- Docker Compose 2.28.1
- Docker 27.0.3
- git 2.45.2
- bash 5.2.26
2. Убедитесь что порт 8000 свободен
2. Выполните команду:
```bash
git clone https://github.com/wumpscut0/cars.git ./cars_wumpscut0 && cd ./cars_wumpscut0 && docker-compose up --build
```

### local
1. Убедитесь, что в системе установлены (Версии могут отличаться):
- git 2.45.2
- bash 5.2.26
- poetry 1.8.3 или pip 24.2
2. Убедитесь что порт 8000 свободен
3. Выполните команду
   - вариант poetry:
   ```bash
   git clone https://github.com/wumpscut0/cars.git ./cars_wumpscut0 && cd ./cars_wumpscut0 && poetry install && poetry shell
   ```
   ```bash
   python manage.py makemigrations && python manage.py migrate && python manage.py runserver
   ```    
   - вариант pip:
   ```bash
   git clone https://github.com/wumpscut0/cars.git ./cars_wumpscut0 && cd ./cars_wumpscut0 && python -m venv .venv_CfRhiWwupo && source .venv_CfRhiWwupo/bin/activate
   ```
   ```bash
   pip install -r requirements.txt && python manage.py makemigrations && python manage.py migrate && python manage.py runserver
   ```
## Доступ к приложению
### Главная страница: http://127.0.0.1:8000
### Документация API: http://127.0.0.1:8000/api/docs

## Команда проекта
- Всеволод Богдашов — Web-developer
