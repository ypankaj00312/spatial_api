# Spatial API with FastAPI and GeoAlchemy2

This project demonstrates a simple spatial API built using FastAPI, SQLAlchemy, and GeoAlchemy2 for handling geospatial data in a PostgreSQL database with the PostGIS extension.

## Getting Started

These instructions will guide you on how to set up and run the API locally.

### Prerequisites

*   Python 3.9+
*   pip
*   A virtual environment (recommended)
*   PostgreSQL with the PostGIS extension enabled
*   Alembic (optional, for database migrations)

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/ypankaj00312/spatial_api.git
    ```

2.  **Create a Virtual Environment:**

    ```bash
    python3 -m venv .venv  # Or use conda: conda create -n myenv python=3.9
    source .venv/bin/activate  # On Linux/macOS. On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install fastapi uvicorn sqlalchemy geoalchemy2 psycopg2 python-dotenv pydantic
    ```

4.  **Database Setup:**

    *   **PostgreSQL with PostGIS:** Ensure you have PostgreSQL installed and the PostGIS extension is enabled in your database.  
    *   **Create Database:** Create a database (e.g., `spatial_db`).
    *   replace your database credentials in app/database.py:

        ```bash
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_HOST=your_db_host  # e.g., localhost
        DB_NAME=spatial_db
        ```

5.  **Run the Application:**

    ```bash
    uvicorn main:app --reload  # Replace main:app with the correct path if necessary
    ```

    The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### Points

*   **POST /points/**: Create a new point.
    **PUT /points/{Point_id}**:
    ```json
    {
      "name": "My Point",
      "description": "A point of interest",
      "longitude": -77.0369,
      "latitude": 38.8075
    }
    ```

*   **GET /points/**: List all points.

### Polygons

*   **POST /polygons/**: Create a new polygon.
    **PUT /polygons/{Polygon_id}**:

    ```json
    {
      "name": "My Polygon",
      "description": "A polygon area",
      "coordinates": [[[-77.05, 38.9], [-77.06, 38.91], [-77.07, 38.9], [-77.06, 38.89], [-77.05, 38.9]]],
      "population_density": 150
    }
    ```

*   **GET /polygons/**: List all polygons.

