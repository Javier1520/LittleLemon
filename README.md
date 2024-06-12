# Restaurant LittleLemon API Documentation

This API provides endpoints for managing categories, menu items, carts, orders, and user groups in a restaurant management system.

# Instructions to Run the Application

## Ensure Docker and Docker Compose are installed:

- **Docker:** [Get Docker](https://docs.docker.com/get-docker/)
- **Docker Compose:** [Install Docker Compose](https://docs.docker.com/compose/install/)

### Development's versions:
- Docker version 26.1.1, build 4cf5afa
- Docker Compose version v2.27.1

## Build and run the application:

1. Open a terminal.
2. Navigate to the project directory (where the `Dockerfile` and `docker-compose.yaml` are located).
3. Run the following command:

    ```sh
    docker-compose up --build
    ```

    This command will build the Docker images and start the containers. The `--build` flag forces the build of the images before starting the containers.

## Access the application:

Once the containers are up and running, you can access the Django application at [http://localhost:8000](http://localhost:8000).

## Additional Information

### Environment Variables:

- `PYTHONDONTWRITEBYTECODE`: Prevents Python from writing `.pyc` files to disk.
- `PYTHONUNBUFFERED`: Ensures that Python output is logged directly to the terminal without buffering.

### Volumes:

The `volumes` directive in `docker-compose.yaml` ensures that any changes in your local directory are reflected inside the container immediately. This is useful for development purposes.

### Database:

- The `db` service uses the official PostgreSQL image.
- The environment variables set the database name, user, and password.
- The `volumes` directive ensures that the database data is persisted even when the container is restarted.

## Useful Commands

- **Stopping the containers:**

    ```sh
    docker-compose down
    ```

- **Rebuilding the containers:**

    ```sh
    docker-compose up --build
    ```

- **Accessing the Django shell:**

    ```sh
    docker-compose run web python manage.py shell
    ```

- **Creating a superuser:**

    ```sh
    docker-compose run web python manage.py createsuperuser
    ```

## Authentication Endpoints

The authentication endpoints are provided by the `djoser` library and are included in the API URLs.

- `POST /api/auth/users/`: Register a new user.
- `POST /api/auth/token/login/`: Obtain an authentication token.
- `POST /api/auth/token/logout/`: Logout and invalidate the authentication token.

For more information on the available authentication endpoints, refer to the [Djoser documentation](https://djoser.readthedocs.io/en/latest/getting_started.html).

## Category Endpoints

- `GET /api/categories`: Retrieve a list of all categories.
- `POST /api/categories`: Create a new category. (Requires Manager role)
- `GET /api/categories/<int:pk>`: Retrieve details of a specific category.
- `PUT /api/categories/<int:pk>`: Update a specific category. (Requires Manager role)
- `DELETE /api/categories/<int:pk>`: Delete a specific category. (Requires Manager role)

## Menu Item Endpoints

- `GET /api/menu-items`: Retrieve a list of all menu items with filtering and pagination support.
- `POST /api/menu-items`: Create a new menu item. (Requires Manager role)
- `GET /api/menu-items/<int:pk>`: Retrieve details of a specific menu item.
- `PUT /api/menu-items/<int:pk>`: Update a specific menu item. (Requires Manager role)
- `DELETE /api/menu-items/<int:pk>`: Delete a specific menu item. (Requires Manager role)

## Cart Endpoints

- `GET /api/cart/menu-items`: Retrieve the cart items for the authenticated user.
- `POST /api/cart/menu-items`: Add a menu item to the authenticated user's cart.
- `DELETE /api/cart/menu-items`: Clear the authenticated user's cart.

## Order Endpoints

- `GET /api/orders`: Retrieve a list of orders with filtering and pagination support. Managers can see all orders, delivery crew can see their assigned orders, and regular users can see their own orders.
- `POST /api/orders`: Create a new order for the authenticated user.
- `GET /api/orders/<int:pk>`: Retrieve details of a specific order. Managers can see any order, delivery crew can see their assigned orders, and regular users can see their own orders.
- `PATCH /api/orders/<int:pk>`: Update the status of a specific order. Managers can assign a delivery crew member, and delivery crew can mark an order as delivered.
- `DELETE /api/orders/<int:pk>`: Delete a specific order. (Requires Manager role)

## User Group Management Endpoints

- `GET /api/groups/manager/users`: Retrieve a list of users in the Manager group. (Requires Manager role)
- `POST /api/groups/manager/users`: Add a user to the Manager group. (Requires Manager role)
- `DELETE /api/groups/manager/users/<int:pk>`: Remove a user from the Manager group. (Requires Manager role)
- `GET /api/groups/delivery-crew/users`: Retrieve a list of users in the Delivery Crew group. (Requires Manager role)
- `POST /api/groups/delivery-crew/users`: Add a user to the Delivery Crew group. (Requires Manager role)
- `DELETE /api/groups/delivery-crew/users/<int:pk>`: Remove a user from the Delivery Crew group. (Requires Manager role)

## Request and Response Formats

All requests and responses use JSON format.

### Category Request/Response Format

```json
{
    "id": 1,
    "slug": "appetizers",
    "title": "Appetizers"
}
```

### Menu Item Request Format

```json
{
    "title": "Garlic Bread",
    "price": 4.99,
    "featured": true,
    "category_id": 1
}
```

### Menu Item Response Format

```json
{
    "id": 1,
    "title": "Garlic Bread",
    "price": "4.99",
    "featured": true,
    "category": {
        "id": 1,
        "slug": "appetizers",
        "title": "Appetizers"
    },
    "category_id": 1
}
```

### Cart Request Format

```json
{
    "menuitem_id": 1,
    "quantity": 2
}
```

### Cart Response Format

```json
{
    "id": 1,
    "user": 1,
    "menuitem": {
        "id": 1,
        "title": "Garlic Bread",
        "price": "4.99",
        "featured": true,
        "category": {
            "id": 1,
            "slug": "appetizers",
            "title": "Appetizers"
        },
        "category_id": 1
    },
    "menuitem_id": 1,
    "quantity": 2,
    "unit_price": "4.99",
    "price": "9.98"
}
```

### Order Response Format

```json
{
    "id": 1,
    "user": 1,
    "user_id": 1,
    "delivery_crew": "john_doe",
    "delivery_crew_id": 2,
    "status": true,
    "total": "14.97",
    "date": "08/06/2024 - 18:30:00",
    "order_items": [
        {
            "id": 1,
            "menuitem": {
                "id": 1,
                "title": "Garlic Bread",
                "price": "4.99",
                "featured": true,
                "category": {
                    "id": 1,
                    "slug": "appetizers",
                    "title": "Appetizers"
                },
                "category_id": 1
            },
            "menuitem_id": 1,
            "quantity": 2,
            "unit_price": "4.99",
            "price": "9.98"
        },
        {
            "id": 2,
            "menuitem": {
                "id": 2,
                "title": "Caesar Salad",
                "price": "4.99",
                "featured": false,
                "category": {
                    "id": 2,
                    "slug": "salads",
                    "title": "Salads"
                },
                "category_id": 2
            },
            "menuitem_id": 2,
            "quantity": 1,
            "unit_price": "4.99",
            "price": "4.99"
        }
    ]
}
```


## Installation without docker
### Install pipenv
```
python3 -m pip install --user pipenv
```
### Create pipenv environment
```
pipenv shell
```
### Install dependencies
```
pipenv install
```
### Run server
```
python3 manage.py runserver
```
