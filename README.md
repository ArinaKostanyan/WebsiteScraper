# Property Scraper & Interested List API Requirements

## Overview
We are going to scrape the floorplan data of some properties sites using LLMs. System scrapes property names, floorplan information, and prices from a list of websites using the ScrapegraphAI tool. It provides an API to retrieve floorplan data based on filters, also manages user interested lists, and handles user data.

## Technology Stack
- **Backend**: Python FastAPI
- **Database**: MySQL for production
- **Web Scraping**: ScrapegraphAI (https://github.com/ScrapeGraphAI/Scrapegraph-ai)
- **ORM**: sqlalchemy
- **API Documentation**: Swagger (via FastAPI)
---
## 1. Data Scraping

This project uses Ollama as an AI model provider to enhance the scraping process and make intelligent decisions during data extraction. Ollama allows you to access and utilize large language models (LLMs) to interact with and process data in a more flexible and robust way.

### How to Use Ollama
To get started with Ollama in this project, follow these steps:

* Install Ollama: Make sure you have Ollama installed on your system. You can download and install it from [the official Ollama website](https://ollama.com/).
* Once installed, you can check if it's working by running:
 ```
ollama version
```
* To run the Ollama server, you can use the following command:
```
ollama run llama3.2
```

#### List of Property Websites:
1. https://www.atmospheretempe.com/floor-plans/
2. https://clemsonlivingsc.com/the-orchard/
3. https://rambleratlanta.com/floorplans/
4. https://www.millenniumok.com/floor-plans/
5. https://www.churchandhenley.com/floor-plans/
6. https://pavilion-berry.com/rates-floorplans/
7. https://mapleridgeblacksburg.com/all-floor-plans/
8. https://current-latimer.com/rates-floorplans/



### 1.2 Required Fields
Each property should have the following fields:
- `property_name` – Name of the property
- `website` – Source website of the property

Each floorplan should have the following fields:
- `floorplan_name` – Name of the floorplan
- `price` – Price of the floorplan (NULL if not available)
- `number_of_bedrooms` – Number of bedrooms (NULL if not available)
- `number_of_bathrooms` – Number of bathrooms (NULL if not available)
- `square_feet` – Square footage of the floorplan (NULL if not available)

If any field is absent, it should be stored as `NULL`.

---

## 2. API Endpoints

### 2.1 Get Floorplans by Filters
**Endpoint:** `GET /floorplans`

**Query Parameters:**
- `price_min`, `price_max`
- `number_of_bedrooms`
- `number_of_bathrooms`
- `square_feet_min`, `square_feet_max`

### 2.2 Get Property's Floorplans by Name
**Endpoint:** `GET /floorplans/{property_name}`

### 2.3 Get Floorplan by Name & Property Name
**Endpoint:** `GET /floorplans/{property_name}/{floorplan_name}`

---

## 3. User Management

### 3.1 Add User
**Endpoint:** `POST /users`

**Request Body:**
```json
{
    "name": "John Doe"
}
```

### 3.2 Get User by ID
**Endpoint:** `GET /users/{user_id}`

---

## 4. Interested List Management

### 4.1 Add Floorplan to User’s Interested List
**Endpoint:** `POST /interested`

**Request Body:**
```json
{
    "user_id": 1,
    "floorplan_name": "Deluxe Suite",
    "property_name": "Sunset Apartments"
}
```

### 4.2 Get User’s Interested List
**Endpoint:** `GET /interested/{user_id}`

### 4.3 Remove Floorplan(s) from Interested List
**Endpoint:** `DELETE /interested`

**Request Body:**

removes only the floorplan "Deluxe Suite" of the property "Sunset Apartments"

```json
{
    "user_id": 1,
    "floorplan_name": "Deluxe Suite",
    "property_name": "Sunset Apartments"
}
```
**OR**

removes all flooplans of the property "Sunset Apartments"

```json
{
    "user_id": 1,
    "property_name": "Sunset Apartments"
}
``` 

---

## 5. Database Structure
Design a Database Structure that fits the best of the requirements of the API.


## Prerequisites

Before you start, make sure you have the following installed:

Python 3.8+
Poetry (for dependency management)
MySQL (or SQLite for development)
Uvicorn (for running the FastAPI application)

## Setup Instructions

1. Clone the repository
```
git clone https://github.com/ArinaKostanyan/WebsiteScraper
cd WebsiteScrapper
```
2. Install dependencies with Poetry
Make sure Poetry is installed. If not, you can install it by running:
```
curl -sSL https://install.python-poetry.org | python3 -
```
Then, install the dependencies:
```
poetry install
```
3. Configure your MySQL database
Make sure you have MySQL running locally (or use any other MySQL-compatible database). Update the DATABASE_URL in your db.py:
```
DATABASE_URL = "mysql+pymysql://<username>:<password>@localhost/<database>"
```
## Run the FastAPI app
Now you can start the FastAPI app using Uvicorn:
```
python app.py
```
The app should now be accessible at http://127.0.0.1:8000.

6. Access the API Documentation
You can access the interactive Swagger documentation for the API by visiting:

http://127.0.0.1:8000/docs

## Run tests
```
python -m pytest tests/test_main_app.py
```