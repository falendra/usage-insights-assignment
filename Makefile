.PHONY: setup start-backend start-frontend test

setup:
	@echo "==> Setting up backend..."
	cd backend && python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt && \
	python manage.py migrate
	@echo "==> Setting up frontend..."
	cd frontend && npm install

start-backend:
	@echo "==> Starting Django backend on port 8000..."
	cd backend && . venv/bin/activate && python manage.py runserver

start-frontend:
	@echo "==> Starting React frontend on port 5173..."
	cd frontend && npm run dev

test:
	@echo "==> Running backend tests..."
	cd backend && . venv/bin/activate && pytest usage_insights/tests.py -v

migrate:
	@echo "==> Running migrations..."
	cd backend && . venv/bin/activate && python manage.py migrate

reset-db:
	@echo "==> Resetting database..."
	rm -f backend/db.sqlite3
	$(MAKE) migrate
