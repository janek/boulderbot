all:
	@echo Usage:
	@echo make test
	@echo make run

test:
	pytest --log-cli-level INFO

run:
	python3 boulderbot.py

heroku-pause:
	heroku maintenance:on -a ricchardo-bukowski

heroku-unpause:
	heroku maintenance:off -a ricchardo-bukowski

heroku-log:
	heroku logs --tail -a ricchardo-bukowski
