#!/bin/bash

# Deployment script for Cybersecurity Fraud Detection System

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Fraud Detection System Setup${NC}"
echo -e "${BLUE}================================${NC}\n"

# Check if Docker is installed
echo -e "${YELLOW}Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker found${NC}\n"

# Check if Docker Compose is installed
echo -e "${YELLOW}Checking Docker Compose installation...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install it first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker Compose found${NC}\n"

# Create .env file if it doesn't exist
echo -e "${YELLOW}Setting up environment variables...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file from .env.example${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Create necessary directories
echo -e "${YELLOW}Creating necessary directories...${NC}"
mkdir -p logs models data/training_data
echo -e "${GREEN}✓ Directories created${NC}\n"

# Build Docker images
echo -e "${YELLOW}Building Docker images...${NC}"
docker-compose build
echo -e "${GREEN}✓ Docker images built${NC}\n"

# Start services
echo -e "${YELLOW}Starting services...${NC}"
docker-compose up -d
echo -e "${GREEN}✓ Services started${NC}\n"

# Wait for services to be healthy
echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
sleep 10

# Check service health
echo -e "${YELLOW}Checking service status...${NC}"
docker-compose ps
echo -e "${GREEN}✓ Services are running${NC}\n"

# Display API information
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}\n"

echo -e "${BLUE}API Information:${NC}"
echo -e "  Base URL: ${BLUE}http://localhost:8000${NC}"
echo -e "  Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo -e "  ReDoc: ${BLUE}http://localhost:8000/redoc${NC}\n"

echo -e "${BLUE}Database Information:${NC}"
echo -e "  Host: ${BLUE}localhost${NC}"
echo -e "  Port: ${BLUE}5432${NC}"
echo -e "  User: ${BLUE}fraud_user${NC}"
echo -e "  Database: ${BLUE}fraud_detection_db${NC}\n"

echo -e "${BLUE}Redis Information:${NC}"
echo -e "  Host: ${BLUE}localhost${NC}"
echo -e "  Port: ${BLUE}6379${NC}\n"

echo -e "${BLUE}Monitoring:${NC}"
echo -e "  Prometheus: ${BLUE}http://localhost:9090${NC}"
echo -e "  Grafana: ${BLUE}http://localhost:3000${NC}"
echo -e "    (Default credentials: admin/admin)\n"

echo -e "${YELLOW}Next Steps:${NC}"
echo -e "  1. Update .env with your secure values"
echo -e "  2. Visit ${BLUE}http://localhost:8000/docs${NC} to explore the API"
echo -e "  3. Train ML models with your data"
echo -e "  4. Configure monitoring dashboards in Grafana\n"

echo -e "${GREEN}System is ready to use!${NC}\n"
