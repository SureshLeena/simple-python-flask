A simple Flask API service with PostgreSQL database integration.

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL

### Installation

1. Clone this repository

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database
- Run the SQL commands in `db_setup.sql` to create the database and required tables and sample data
- Update the `.env` file with your database credentials

5. Start the application
```bash
python src/app.py
```

The server will start at http://localhost:5001

## API Endpoints

### Health Check
- **GET** `/api/health` - Check if the service is running

### Items
- **GET** `/api/items` - Get all items
- **GET** `/api/items/{item_id}` - Get a specific item by ID
- **POST** `/api/items` - Add a new item
- **PUT** `/api/items/{item_id}` - Update an existing item
- **DELETE** `/api/items/{item_id}` - Delete an item

## Example Requests

### Get all items
```bash
curl -X GET http://localhost:5001/api/items
```

### Get a specific item
```bash
curl -X GET http://localhost:5001/api/items/1
```

### Add a new item
```bash
curl -X POST http://localhost:5001/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Tablet", "description": "10-inch tablet with 128GB storage", "price": 349.99}'
```

### Update an item
```bash
curl -X PUT http://localhost:5001/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Premium Laptop", "price": 1499.99}'
```

### Delete an item
```bash
curl -X DELETE http://localhost:5001/api/items/5
```