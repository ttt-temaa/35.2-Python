# DRF Project

## Описание проекта
Проект представляет собой веб-приложение на Django REST Framework с настройкой CI/CD и автоматическим деплоем.

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

## Локальная разработка

### Предварительные требования
- Python 3.10
- Poetry (для управления зависимостями)
- Docker и Docker Compose (опционально)

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
.venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
poetry install
# или
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта:
```env
SECRET_KEY=your-secret-key
POSTGRES_DB=your-db-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Запустите сервер разработки:
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

## Поддержка

При возникновении проблем создайте issue в репозитории проекта. 