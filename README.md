# Netflix Database

This repository contains the script to generate database to ingest csv data and API for manipulating Netflix database. The data was sourced from Kaggle and is structured according to an Entity-Relationship Diagram (ERD) included in the repository. The database is managed using PostgreSQL.

## Dataset URL

[Netflix Dataset (kaggle.com)](https://www.kaggle.com/datasets/thedevastator/the-ultimate-netflix-tv-shows-and-movies-dataset?select=Best+Shows+Netflix.csv)

## Prerequisites

Before you begin, ensure you have the following installed:

- PostgreSQL (Version 12.0 or newer recommended)
- pgAdmin 4 (or another PostgreSQL client)
- Python 3.8 or newer
- pip (Python package installer)

## Installation Guide

### 1. Clone the Repository

Start by cloning this repository to your local machine using:

```bash
git clone https://github.com/TuringCollegeSubmissions/martstelm-DE1.v2.4.1
cd martstelm-DE1.v2.4.1
```

### 2. Set Up Python Environment

Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Create database

Then, create a new database in PostgreSQL:

```sql
CREATE DATABASE netlfic;
```

### 4. Configure Environment Variables

Create a .env file in the src directory of your project and add the following environment variables to configure your database connection:

```bash
cd src/
```

```env
DB_NAME=netflix
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
```

### 5. Run application

Copy csv file into src folder and run python application

```bash
python csv_insertion.py
```

### 6. Verify the Import

To verify that the data has been imported successfully, you can run the following SQL query:

```sql
SELECT *
FROM public.movie
LIMIT 10;
```

## Usage

You can now use pgAdmin or any other PostgreSQL client to connect to the `good_reads_books` database and run queries, generate reports, or perform analysis.

# API

## Get started

To run the API and communicate with database, run python script:

```bash
python main.py
```

## GET requests

To get data from movie or show databases, there is to endpoints you can use

### Movie

#### Return all movies

```bash
curl -X GET http://127.0.0.1:8002/movie/all
```

#### Return movies by id

```bash
curl -X GET http://127.0.0.1:8002/movie/{movie_id}
```

### Show

#### Return all shows

```bash
curl -X GET http://127.0.0.1:8002/show/all
```

#### Return shows by id

```bash
curl -X GET http://127.0.0.1:8002/show/{show_id}
```
