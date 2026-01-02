#!/usr/bin/env python3
"""
Flask REST API application with PostgreSQL and Redis
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import redis
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://appuser:apppassword@postgres:5432/appdb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True
)

# Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# Routes
@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Check database
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    try:
        # Check Redis
        redis_client.ping()
        redis_status = 'healthy'
    except Exception as e:
        redis_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'redis': redis_status,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users with caching"""
    # Check cache first
    cached = redis_client.get('users:all')
    if cached:
        return jsonify(json.loads(cached))
    
    # Query database
    users = User.query.all()
    result = [user.to_dict() for user in users]
    
    # Cache for 60 seconds
    redis_client.setex('users:all', 60, json.dumps(result))
    
    return jsonify(result)

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Username and email required'}), 400
    
    try:
        user = User(
            username=data['username'],
            email=data['email']
        )
        db.session.add(user)
        db.session.commit()
        
        # Invalidate cache
        redis_client.delete('users:all')
        
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if data.get('username'):
        user.username = data['username']
    if data.get('email'):
        user.email = data['email']
    
    try:
        db.session.commit()
        redis_client.delete('users:all')
        return jsonify(user.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        redis_client.delete('users:all')
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Run application
    app.run(host='0.0.0.0', port=5000, debug=False)
