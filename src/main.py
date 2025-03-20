from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from database import Database
from ai_engine import AIEngine

app = Flask(__name__)

# Path to store database configuration
CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'db_config.json')

# Ensure config directory exists
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

# Database and AI engine instances
db = None
ai_engine = None

def load_db_config():
    """Load database configuration from file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def save_db_config(config):
    """Save database configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def initialize_db():
    """Initialize database connection"""
    global db, ai_engine
    config = load_db_config()
    if config:
        try:
            db = Database(config)
            ai_engine = AIEngine(db)
            return True
        except Exception as e:
            print(f"Error initializing database: {e}")
    return False

@app.route('/')
def index():
    """Main page route"""
    # Check if database is configured
    if not initialize_db():
        return redirect(url_for('database_config'))
    return render_template('index.html')

@app.route('/database-config')
def database_config():
    """Database configuration page route"""
    return render_template('database_config.html')

@app.route('/config', methods=['POST'])
def config():
    """Handle database configuration submission"""
    global db, ai_engine
    
    config = request.json
    
    try:
        # Test connection with provided config
        test_db = Database(config)
        test_db.test_connection()
        
        # Save configuration if connection successful
        save_db_config(config)
        
        # Initialize with new config
        db = test_db
        ai_engine = AIEngine(db)
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/query', methods=['POST'])
def query():
    """Handle AI query submission"""
    if not db or not ai_engine:
        if not initialize_db():
            return jsonify({"success": False, "error": "Database not configured"})
    
    query = request.json.get('query', '')
    
    try:
        response = ai_engine.process_query(query)
        return jsonify({"success": True, "response": response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)