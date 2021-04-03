# Makefile: common make commands used for local development

# Install requirements
.PHONY: requirements
requirements:
	@pip install -r requirements.txt


########################
# Development Commands #
########################

.PHONY: run-scraper
run-scraper:
	PYTHONPATH=. python scraper/main.py

# Run Celery Worker
.PHONY: run-parser
run-parser:
	PYTHONPATH=. python scraper/parse.py
