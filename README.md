# Document Retrieval System

## About the Project

An efficient keyword-based Document Retrieval System that allows users to upload text documents, search for documents based on keywords and phrases, and retrieve results ranked by relevance using TF-IDF scoring. The system is designed with performance in mind and includes features like caching for repeated queries and a clean, interactive frontend.

## Tech Stack

* **Backend**: Django 4.2.10
* **Frontend**: React.js
* **Database**: MySQL 8.0 (or MariaDB 10.5+)
* **API Documentation**: Swagger (drf-yasg)
* **Text Processing**: spaCy (English Model)

## Features

* Upload text (.txt) documents
* Full-text search with keyword matching
* TF-IDF-based relevance scoring
* Caching of repeated searches for performance
* API Documentation with Swagger UI
* User-friendly frontend for search and upload
* Clean project architecture

## Screenshots

![Swagger UI Screenshot](#)
![Search Frontend Screenshot](#)
![Upload Document Frontend Screenshot](#)

*(You can replace # with your actual image links if hosted or local paths.)*

## Architecture

```
React Frontend
    |
    |-- Axios HTTP Requests
    |
Django Backend (API Server)
    |
    |-- Upload API --> Document Table --> Inverted Index Table
    |-- Search API --> Query Tokens --> TF-IDF Relevance Ranking
    |-- Caching Layer --> Faster repeated searches
    |
MySQL Database (for metadata storage)
```

## Prerequisites

* Python 3.9+
* Node.js 18+
* MySQL Server 8.0+
* pip package manager

Install required Python packages:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend/document-search-frontend
npm install
```

Ensure MySQL is running and your database credentials are configured in `settings.py`.

## Running Locally (Demo)

1. **Start Backend**

```bash
cd backend/doc_retrieval_system
python manage.py runserver
```

Visit `http://127.0.0.1:8000/swagger/` for Swagger API docs.

2. **Start Frontend**

```bash
cd frontend/document-search-frontend
npm start
```

Visit `http://localhost:3000/` to use the React frontend.

## API Documentation (Swagger)

* Swagger UI: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
* ReDoc (optional): [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

**Endpoints:**

* **POST** `/api/upload/` - Upload a new document
* **GET** `/api/search/?q=keyword` - Search documents
* **POST** `/api/rebuild-index/` - Rebuild the full inverted index

## Deployment

You can deploy this project using:

* **Backend**: Render, Railway, Heroku
* **Frontend**: Vercel, Netlify

Deployment tips:

* Use managed MySQL hosting (like PlanetScale) in production.
* Set up CORS policy in Django settings.
* Use environment variables for Django `SECRET_KEY`, DB credentials.

## Project Structure (Tree View)

```
document-retrieval-system/
├── backend/
│   ├── doc_retrieval_system/
│       ├── settings.py
│       ├── urls.py
│       ├── wsgi.py
│   ├── document_search/
│       ├── models.py
│       ├── views.py
│       ├── utils.py
│       ├── urls.py
│       ├── migrations/
├── frontend/
    ├── document-search-frontend/
        ├── src/
            ├── App.js
            ├── pages/
                ├── SearchPage.jsx
                ├── UploadPage.jsx
            ├── components/
                ├── Navbar.jsx
```

## License

Distributed under the BSD 3-Clause License.

## Contact

* **Developer**: Modisa Nallaperuma
* **Email**: [modisanallaperum@gmail.com](mailto:modisanallaperum@gmail.com)

---
