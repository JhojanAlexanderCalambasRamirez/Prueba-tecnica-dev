# Backend (Django + DRF) – Esqueleto mínimo

## Requisitos
- Python 3.10+ recomendado
- (Opcional) Entorno virtual

## Instalación
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
- API base en: http://127.0.0.1:8000/
- Salud: http://127.0.0.1:8000/health/
- TICKETS: http://127.0.0.1:8000/api/tickets/

## Base de datos (SQLite por defecto)
- El backend usa SQLite (archivo `backend/db.sqlite3`).
- No requiere instalar servicios externos.
- Comandos:
  - Migraciones: `python manage.py migrate`
  - Semillas: `python manage.py seed_helpdesk` (opcional)
  - Superusuario: `python manage.py createsuperuser` (opcional)
