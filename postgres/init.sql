-- Initialize database with extensions and basic setup

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create initial schema (tables created by Flask SQLAlchemy)

-- Create indexes for performance
-- Will be added after tables exist

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE appdb TO appuser;
