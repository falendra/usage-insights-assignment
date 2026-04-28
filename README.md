# Usage Insights SaaS Feature

This project is a take-home assignment implementation for a Usage Insights feature.

## Structure
- `backend/`: Django backend with DRF.
- `frontend/`: React frontend with Vite.

## Backend Setup
1. Navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install django djangorestframework django-cors-headers`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

## Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`
