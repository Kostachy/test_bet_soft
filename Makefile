package_dir := "src"

.PHONY: up
up:  ## Run app in docker container
	docker compose up --build -d

.PHONY: down
down:  ## Stop docker containers
	docker compose down

.PHONY: migrate
migrate:  ## migrate last migrations to head
	docker compose exec bet_maker alembic upgrade head
