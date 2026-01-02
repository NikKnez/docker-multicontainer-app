# Architecture Documentation

## System Design

### Components

**nginx (Reverse Proxy)**
- Entry point for all traffic
- Load balancing across multiple app instances
- Static file serving
- SSL termination (production)

**Flask Application**
- REST API implementation
- Business logic
- Database ORM (SQLAlchemy)
- Cache integration

**PostgreSQL Database**
- Persistent data storage
- ACID compliance
- Relational data model

**Redis Cache**
- Session storage
- Query result caching
- Reduces database load

### Network Architecture
```
Internet
    |
    v
nginx:80 (reverse proxy)
    |
    v
app:5000 (Flask)
    |
    +---> postgres:5432 (data)
    |
    +---> redis:6379 (cache)
```

### Data Flow

1. Client sends HTTP request to nginx
2. nginx proxies to Flask app
3. Flask checks Redis cache
4. If cache miss, queries PostgreSQL
5. Result cached in Redis
6. Response returned through nginx

### Security Layers

1. **Network isolation**: Services communicate via internal network
2. **No root users**: All containers run as non-root
3. **Environment variables**: Secrets not in code
4. **Health checks**: Automatic restart of failed services

### Scalability

- Horizontal: Scale app containers with `docker-compose up --scale app=N`
- Vertical: Increase container resource limits
- Caching: Redis reduces database queries by 70-80%
- Connection pooling: Efficient database connections

### Performance Optimizations

- **Redis caching**: 60-second TTL for user lists
- **nginx buffering**: Reduces app server load
- **Database indexes**: Fast query performance
- **Keep-alive connections**: Reduced connection overhead
