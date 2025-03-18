# Property Scraper & Interested List API Requirements

## Overview
We are going to scrape the floorplan data of some properties sites using LLMs. System scrapes property names, floorplan information, and prices from a list of websites using the ScrapegraphAI tool. It provides an API to retrieve floorplan data based on filters, also manages user interested lists, and handles user data.

## Technology Stack
- **Backend**: Python (Django or FastAPI)
- **Database**: SQLite (or PostgreSQL/MySQL for production)
- **Web Scraping**: ScrapegraphAI (https://github.com/ScrapeGraphAI/Scrapegraph-ai)
- **ORM**: Django or sqlalchemy
- **API Documentation**: Swagger (via Django or FastAPI)
---
## 1. Data Scraping

### 1.1 Scraping Details
- **Source**: Given list of property websites
- **Tool**: ScrapegraphAI

#### List of Property Websites:
1. https://www.atmospheretempe.com/floor-plans/
2. https://clemsonlivingsc.com/the-orchard/
3. https://rambleratlanta.com/floorplans/
4. https://www.millenniumok.com/floor-plans/
5. https://www.churchandhenley.com/floor-plans/
6. https://pavilion-berry.com/rates-floorplans/
7. https://mapleridgeblacksburg.com/all-floor-plans/
8. https://current-latimer.com/rates-floorplans/

- **Source**: Given list of property websites
- **Tool**: ScrapegraphAI
- **Method**: Scraping via ScrapegraphAI

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