# Dockerized Multi-Container Application

Production-ready multi-container application using Docker Compose. Demonstrates containerization, networking, and orchestration skills.

## Architecture
```
nginx (reverse proxy) :80
    |
    v
app (Python Flask) :5000
    |
    v
postgres (database) :5432
    |
    v
redis (cache) :6379
```

## Components

**nginx**: Reverse proxy and load balancer
- Handles SSL termination
- Serves static files
- Proxies API requests to Flask app

**app**: Python Flask REST API
- User authentication
- CRUD operations
- Database interactions
- Redis caching

**postgres**: PostgreSQL database
- Persistent data storage
- Automated backups

**redis**: Redis cache
- Session storage
- Query result caching

## Features

- Container networking with Docker Compose
- Persistent volumes for database
- Health checks for all services
- Environment-based configuration
- Automated database migrations
- Logging aggregation
- Development and production modes

## Requirements

- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- Linux/macOS/WSL2

## Quick Start
```bash
# Clone repository
git clone https://github.com/NikKnez/docker-multicontainer-app.git
cd docker-multicontainer-app

# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f

# Access application
curl http://localhost/api/health
```

## Project Structure
```
.
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── models.py
│   └── config.py
├── nginx/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── default.conf
├── postgres/
│   └── init.sql
├── scripts/
│   ├── backup-database.sh
│   ├── restore-database.sh
│   └── health-check.sh
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
└── README.md
```

## Usage

### Development Mode
```bash
# Start services
docker-compose up

# Run with rebuild
docker-compose up --build

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Production Mode
```bash
# Use production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale application containers
docker-compose up -d --scale app=3
```

### Database Operations
```bash
# Backup database
./scripts/backup-database.sh

# Restore database
./scripts/restore-database.sh backup-20250101.sql

# Connect to database
docker-compose exec postgres psql -U appuser -d appdb
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app

# Last 100 lines
docker-compose logs --tail=100
```

## API Endpoints

**Health Check**
```bash
GET /api/health
```

**User Management**
```bash
POST /api/users          # Create user
GET  /api/users          # List users
GET  /api/users/:id      # Get user
PUT  /api/users/:id      # Update user
DELETE /api/users/:id    # Delete user
```

**Authentication**
```bash
POST /api/auth/login     # Login
POST /api/auth/logout    # Logout
```

## Configuration

Copy `.env.example` to `.env` and configure:
```bash
# Database
POSTGRES_USER=appuser
POSTGRES_PASSWORD=changeme
POSTGRES_DB=appdb

# Application
FLASK_ENV=production
SECRET_KEY=your-secret-key

# Redis
REDIS_URL=redis://redis:6379/0
```

## Monitoring

Health check endpoints:
- nginx: `http://localhost/health`
- app: `http://localhost/api/health`
- postgres: Automatic health checks in docker-compose
- redis: Automatic health checks in docker-compose

## Security Considerations

- All secrets in environment variables (never in code)
- Database credentials not exposed externally
- Non-root users in containers
- Read-only filesystem where possible
- Regular security updates via base image updates

## Performance

- Redis caching reduces database load
- nginx serves static files efficiently
- Connection pooling in application
- Database indexes on frequently queried fields

## Troubleshooting

**Services won't start:**
```bash
docker-compose down -v
docker-compose up --build
```

**Database connection errors:**
```bash
docker-compose logs postgres
docker-compose exec postgres psql -U appuser -d appdb
```

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8080:80"  # Instead of "80:80"
```

## Development
```bash
# Install development dependencies
docker-compose exec app pip install -r requirements-dev.txt

# Run tests
docker-compose exec app pytest

# Run linter
docker-compose exec app flake8
```

## License

MIT License

## Author

*Nikola Knezevic**
- AWS Certified Cloud Practitioner
- GitHub: [@NikKnez](https://github.com/NikKnez)
- LinkedIn: [Nikola Knezevic](https://linkedin.com/in/nikola-knezevic-devops)
