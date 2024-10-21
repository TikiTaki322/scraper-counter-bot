# SDS Scraper/Weight Counter Telegram bot

## Table of contents
- **[General information](https://github.com/TikiTaki322/scraper-counter-bot#general-information)**
- **[Technologies](https://github.com/TikiTaki322/scraper-counter-bot#technologies)**
- **[Setup](https://github.com/TikiTaki322/scraper-counter-bot#setup)**

## General information
This repository contains the code of a Telegram bot designed to search for SDS documents and calculate cargo weight. It simplifies enterprise workflow by automating operational processes.

## Technologies
#### The technologies used in this project include:
- **Python 3**
- **Aiogram**
- **Selenium**
- **BeautifulSoup 4**
- **PostgreSQL**
- **Redis**

## Setup
To install this repository, follow these steps:

- Open the terminal to create a new directory:
  - mkdir name_of_project
- Navigate into the newly project directory: 
  - cd name_of_project
- Сreate an environment:
  - python -m venv venv
- Activate the virtual environment:
  - for Windows: .\venv\Scripts\activate
  - for Unix: source venv/bin/activate 
- Clone the repository: 
  - git clone https://github.com/tikitaki322/scraper-counter-bot.git
- Navigate into cloned directory:
  - cd scraper-counter-bot
- Create an "input" file in the directory with main.py file with the following variables:
  - TOKEN=<bot_token>
  - ADMIN_ID=<your_telegram_id>
  - DB_USER=postgres
  - DB_PASSWORD=<postgres_password>
  - DB_NAME=<db_name>
  - HOST=<localhost_or_ip>
- Install the required packages: 
  - pip install -r requirements.txt
- Run the project: 
  - python3 main.py


*Before you run it, make sure you have a Redis server running and a Postgres DBMS installed.
- When deploying to Ubuntu>=24.04.1 there is a chance of encountering a problem installing psycopg2, in which case you may need to apply the following commands to build the project:
  - sudo apt install python3.12-dev
  - sudo apt install libpq-dev
  - sudo apt install gcc
