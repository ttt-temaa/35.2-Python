# DRF Project

## Описание проекта
Проект представляет собой веб-приложение на Django REST Framework с настройкой CI/CD и автоматическим деплоем. Проект использует Poetry для управления зависимостями и Docker для контейнеризации.

## Технологии
- Python 3.10
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Nginx
- Gunicorn
- Docker
- GitHub Actions
- Poetry

## Локальная разработка

### Предварительные требования
- Python 3.10
- Poetry
- Docker и Docker Compose (опционально)

### Установка и запуск

1. Активируйте виртуальное окружение:
```bash
poetry shell
```

2. Установите зависимости:
```bash
poetry install
```

3. Создайте файл .env в корневой директории проекта:
```env
SECRET_KEY=your-secret-key
POSTGRES_DB=your-db-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

4. Примените миграции:
```bash
python manage.py migrate
```

5. Запустите сервер разработки:
```bash
python manage.py runserver
```

### Запуск с Docker
```bash
docker-compose up --build
```

## Настройка сервера

### Предварительные требования
- Ubuntu 20.04 LTS или новее
- Python 3.10
- Nginx
- PostgreSQL
- Redis

### Установка на сервер

1. Обновите систему:
```bash
sudo apt update
sudo apt upgrade -y
```

2. Установите необходимые пакеты:
```bash
sudo apt install python3.10 python3.10-venv nginx postgresql redis-server
```

3. Настройте PostgreSQL:
```bash
sudo -u postgres psql
CREATE DATABASE your_db_name;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_user;
```

4. Настройте Nginx:
```bash
sudo nano /etc/nginx/sites-available/your_project
```

Добавьте конфигурацию:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

5. Активируйте конфигурацию Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

6. Настройте Gunicorn:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Добавьте конфигурацию:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/project/.venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

7. Запустите Gunicorn:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## CI/CD

Проект использует GitHub Actions для автоматизации тестирования и деплоя. Workflow запускается при каждом push в репозиторий и включает следующие шаги:

1. Запуск тестов
2. Проверка кода линтером
3. Автоматический деплой на сервер после успешного прохождения тестов

### Настройка GitHub Actions

1. Добавьте следующие секреты в настройках репозитория:
   - `SECRET_KEY`
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `SSH_PRIVATE_KEY`
   - `SERVER_HOST`
   - `SERVER_USER`

2. Workflow файл находится в `.github/workflows/ci.yml`

## Безопасность

1. Настройте файрвол:
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

2. Настройте SSL с Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

## Мониторинг и логирование

- Логи Nginx: `/var/log/nginx/`
- Логи Gunicorn: `/var/log/gunicorn/`
- Логи приложения: `/path/to/your/project/logs/`

## Структура проекта
```
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/
├── materials/
├── docker-compose.yaml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── manage.py
└── .flake8
```

## Поддержка

При возникновении проблем создайте issue в репозитории проекта. 

deploy:
  needs: test
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        script: |
          cd /path/to/your/project
          git pull
          poetry install
          python manage.py migrate
          sudo systemctl restart gunicorn 