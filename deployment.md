# Earthwise Deployment Documentation

This guide covers the production deployment of the Earthwise enterprise backend.

## Architecture
- **Web Server**: Gunicorn
- **ASGI Server**: Daphne (for WebSockets)
- **Database**: PostgreSQL 15
- **Cache/Broker**: Redis
- **Reverse Proxy**: Nginx

## Production Setup

### 1. Environment Variables
Ensure the following are set in your production `.env`:
```env
DEBUG=0
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=api.earthwise.com
DB_NAME=earthwise_prod
DB_USER=earthwise_admin
DB_PASSWORD=secure_password
DB_HOST=db_host
DB_PORT=5432
REDIS_URL=redis://redis_host:6379/1
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 2. Docker Deployment
Use the production-optimized Docker configuration:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### 3. Migrations & Static Files
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### 4. Nginx Configuration (Example)
```nginx
server {
    listen 80;
    server_name api.earthwise.com;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://daphne:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

## Security Best Practices
- Keep `DEBUG=False`.
- Use a strong `SECRET_KEY`.
- Enable HSTS and SSL redirection.
- Regularly rotate database and Redis passwords.
- Monitor `AuditLog` for suspicious activity.

## API Documentation & Postman
The API is fully documented using OpenAPI 3.0 (Swagger).

### Accessing Documentation
- **Swagger UI**: `https://api.earthwise.com/api/docs/`
- **ReDoc**: `https://api.earthwise.com/api/redoc/`
- **Raw Schema**: `https://api.earthwise.com/api/schema/`

### Generating Postman Collection
1.  Navigate to the **Raw Schema** URL (`/api/schema/`).
2.  Save the resulting YAML/JSON file as `earthwise_openapi.json`.
3.  Open Postman and click **Import**.
4.  Upload the `earthwise_openapi.json` file.
5.  Postman will automatically generate a collection with all endpoints, including Authentication, Products, Inventory, and Orders.
