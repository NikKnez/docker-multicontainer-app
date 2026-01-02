# Deployment Guide

## Local Development
```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Production Deployment

### Prerequisites
- Docker and Docker Compose installed
- Domain name configured (optional)
- SSL certificates (for HTTPS)

### Steps

1. Clone repository
```bash
git clone https://github.com/NikKnez/docker-multicontainer-app.git
cd docker-multicontainer-app
```

2. Configure environment
```bash
cp .env.example .env
vim .env  # Edit with production values
```

3. Start services
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

4. Verify deployment
```bash
./scripts/health-check.sh
```

5. Setup automated backups
```bash
# Add to crontab
0 2 * * * /path/to/scripts/backup-database.sh
```

## Scaling
```bash
# Scale Flask app to 3 instances
docker-compose up -d --scale app=3

# nginx will automatically load balance
```

## Monitoring

Check logs:
```bash
docker-compose logs -f app
docker-compose logs -f nginx
docker-compose logs -f postgres
```

Check resource usage:
```bash
docker stats
```

## Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up -d --build
```
