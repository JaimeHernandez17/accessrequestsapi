# Access Requests API

API REST para gestionar solicitudes de acceso a sistemas internos. 

## Setup

### Requisitos
- Python 3.11+
- Docker y Docker Compose (recomendado)

### 🐳 Instalación con Docker (Recomendado)

La forma más rápida de levantar el proyecto:

```bash
docker-compose -f docker-compose.local.yml up --build
```

Esto hará:
- ✅ Construir las imágenes de Django y PostgreSQL
- ✅ Ejecutar migraciones automáticamente
- ✅ Levantar el servidor en `http://localhost:8000`

**Crear superusuario en Docker:**
```bash
docker-compose -f docker-compose.local.yml exec django python manage.py createsuperuser
```

**Ver logs:**
```bash
docker-compose -f docker-compose.local.yml logs -f django
```

**Detener contenedores:**
```bash
docker-compose -f docker-compose.local.yml down
```

### Instalación Local (sin Docker)
1. Crear entorno virtual:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements/local.txt
   ```
   (Nota: Si falla, instalar manualmente: `pip install django djangorestframework djangorestframework-simplejwt django-environ django-allauth[mfa] django-crispy-forms crispy-bootstrap5 drf-spectacular django-cors-headers django-anymail argon2-cffi`)

3. Migraciones:
   ```bash
   python manage.py migrate
   ```

4. Crear superusuario:
   ```bash
   python manage.py createsuperuser
   ```

5. Correr servidor:
   ```bash
   python manage.py runserver
   ```

## Usuarios de Prueba

| Rol | Username | Password |
|---|---|---|
| Admin | admin | admin123 |
| Manager | manager | manager123 |
| Employee | employee | employee123 |

(Debes crear estos usuarios manualmente o usar los tests automatizados).

## Decisiones Técnicas

- **Framework**: Django REST Framework con SimpleJWT para autenticación.
- **Base de Datos**: SQLite para desarrollo local (configurado via `DATABASE_URL`).
- **Permisos**: Clases de permiso personalizadas (`IsEmployee`, `IsManager`, `IsAdmin`) basadas en el campo `role` del usuario.
- **Auditoría**: Modelo `AuditLog` que registra cambios de estado en las solicitudes.
- **Documentación**: Swagger/OpenAPI disponible en `/api/docs/`.

## Tests

Ejecutar tests automatizados:
```bash
pytest accessrequestsapi/access_control/tests/
```
