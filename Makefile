build:
	docker-compose build

migrate:
	docker-compose run app python manage.py migrate --noinput

migrations:
	docker-compose run app python manage.py makemigrations --noinput

ps:
	docker-compose ps

run: docker-compose up -d

restart:
	docker-compose stop
	docker-compose up -d

sh:
	docker-compose run app sh

stop:
	docker-compose stop
