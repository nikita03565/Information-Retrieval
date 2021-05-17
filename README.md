# Information Retrieval
Project is devoted to scraping and analysis of posts data from [pikabu](https://pikabu.ru/).

It consists of several modules (only one for now).

# Scraper
This module collects data from pikabu search, extracts posts content, cleans it from non-relevant information such as 
html tags, punctuation, links, etc.

To start scraper use `make run-scraper` command.

To parse results use `make run-parser` command.

Link to [raw data](https://drive.google.com/file/d/1wks28mEpYz0mcH7P5NFgkbmqD_Lr8e6g/view?usp=sharing).

Links to parsed and filtered data:
[json](https://drive.google.com/file/d/13SpMgAgtzSgak1HAetFyosJ-Ufb3buL1/view?usp=sharing), 
[csv](https://drive.google.com/file/d/1LIPOZzUMQU9jlSAoHAco0Bve_BZp_LDb/view?usp=sharing),
[lemmatized](https://drive.google.com/file/d/1jWbpg2myxov-xp_I5Qpa-GTnU--RtgEY/view?usp=sharing),
[stemmed](https://drive.google.com/file/d/1K4W5FSXAbm2CEw4epmkAUXv12uY9msI-/view?usp=sharing).

Parsed results in json format is a development artifact, we'll use csv for further tasks.
# Exploratory data analysis
Todo

# Classification, clustering, topic modelling
Todo

# Recommendation system
Todo