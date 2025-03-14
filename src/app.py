# app.py
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT", "5432")

# Database connection string
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_db_connection():
    """Create and return a database connection"""
    return psycopg.connect(DB_URL, row_factory=dict_row)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/api/items', methods=['GET'])
def get_items():
    """Fetch all items from the database"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM items ORDER BY id')
                items = cur.fetchall()
                return jsonify({"items": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Fetch a specific item by ID"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM items WHERE id = %s', (item_id,))
                item = cur.fetchone()
                
                if item is None:
                    return jsonify({"error": "Item not found"}), 404
                    
                return jsonify({"item": item})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items', methods=['POST'])
def add_item():
    """Add a new item to the database"""
    try:
        data = request.get_json()
        
        # Simple validation
        if not data or not data.get('name'):
            return jsonify({"error": "Name is required"}), 400
            
        name = data.get('name')
        description = data.get('description', '')
        price = data.get('price', 0)
        
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    'INSERT INTO items (name, description, price) VALUES (%s, %s, %s) RETURNING id, name, description, price, created_at',
                    (name, description, price)
                )
                new_item = cur.fetchone()
                
                return jsonify({"message": "Item added successfully", "item": new_item}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Update an existing item"""
    try:
        data = request.get_json()
        
        # Simple validation
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get existing item to check if it exists
                cur.execute('SELECT * FROM items WHERE id = %s', (item_id,))
                item = cur.fetchone()
                
                if item is None:
                    return jsonify({"error": "Item not found"}), 404
                
                # Update the item
                name = data.get('name', item['name'])
                description = data.get('description', item['description'])
                price = data.get('price', item['price'])
                
                cur.execute(
                    'UPDATE items SET name = %s, description = %s, price = %s WHERE id = %s RETURNING id, name, description, price, created_at',
                    (name, description, price, item_id)
                )
                updated_item = cur.fetchone()
                
                return jsonify({"message": "Item updated successfully", "item": updated_item})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Check if item exists
                cur.execute('SELECT id FROM items WHERE id = %s', (item_id,))
                item = cur.fetchone()
                
                if item is None:
                    return jsonify({"error": "Item not found"}), 404
                
                # Delete the item
                cur.execute('DELETE FROM items WHERE id = %s', (item_id,))
                
                return jsonify({"message": "Item deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure the table exists
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) DEFAULT 0.00,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))