Bloq.it
==============================

Table of Contents
-----------------

-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Running the API](#running-the-api)
-   [Running Tests](#running-tests)
-   [API Documentation](#api-documentation)

Prerequisites
-------------

-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)

Installation
------------

1.  **Clone the repository:**

    `git clone https://github.com/paulocalaes/project_bloq.git
    cd project_bloq`

2.  **Build the Docker containers:**

    `docker compose build`

Running the API
---------------

1.  **Start the containers:**

    `docker-compose up`

    This will start the web server and the database.

2.  **Apply migrations:**

    `docker-compose run web python manage.py migrate`

3.  **Access the API:**

    The API will be available at:

    `http://localhost:8000/api/v1/`

Running Tests
-------------

To run the test suite for all applications:

`docker-compose run web python manage.py test`

To run and generate test coverage report:

`docker compose run web coverage run manage.py test`

To show test coverage:

`docker compose run web coverage report -m`

This will execute all unit tests.

API Documentation
-----------------

Interactive API documentation is available via Swagger UI and ReDoc.

1.  **Swagger UI:**

    `http://localhost:8000/swagger/v1`

2.  **ReDoc UI:**

    `http://localhost:8000/redoc/`