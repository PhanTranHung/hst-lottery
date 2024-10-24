init_env:
	@python3.12 -m venv .vtest


up_db: 
	@docker compose -f ./.docker/docker-compose.database.yaml up -d
	
down_db: 
	@docker compose -f ./.docker/docker-compose.database.yaml down

.PHONY : init_env up_db down_db