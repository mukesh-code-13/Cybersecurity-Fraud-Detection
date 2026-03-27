#!/bin/bash

# Vercel Quick Deploy Script
# Deploy Cybersecurity Fraud Detection System to Vercel

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Vercel Deployment Setup${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}Installing Vercel CLI...${NC}"
    npm install -g vercel
fi

echo -e "${GREEN}✓ Vercel CLI found${NC}\n"

# Check if git is initialized
if [ ! -d .git ]; then
    echo -e "${RED}Error: Git repository not initialized${NC}"
    echo -e "${YELLOW}Run: git init${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Git repository found${NC}\n"

# Check if vercel.json exists
if [ ! -f vercel.json ]; then
    echo -e "${RED}Error: vercel.json not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ vercel.json configured${NC}\n"

# Login to Vercel
echo -e "${YELLOW}Logging in to Vercel...${NC}"
vercel login

# Deploy
echo -e "\n${YELLOW}Deploying to Vercel...${NC}"
vercel

# Get deployment URL
VERCEL_URL=$(vercel --prod 2>/dev/null | grep -o 'https://[^ ]*' | head -1)

if [ -z "$VERCEL_URL" ]; then
    VERCEL_URL="https://your-project.vercel.app"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${BLUE}API URL: ${NC}${VERCEL_URL}\n"

echo -e "${BLUE}Next Steps:${NC}"
echo -e "1. Set environment variables:"
echo -e "   ${YELLOW}vercel env add DATABASE_URL${NC}"
echo -e "   ${YELLOW}vercel env add REDIS_URL${NC}"
echo -e "   ${YELLOW}vercel env add API_KEY${NC}"
echo -e "   ${YELLOW}vercel env add JWT_SECRET${NC}"
echo -e ""
echo -e "2. Redeploy with variables:"
echo -e "   ${YELLOW}vercel --prod${NC}"
echo -e ""
echo -e "3. Test endpoints:"
echo -e "   ${YELLOW}curl ${VERCEL_URL}/api/v1/health${NC}"
echo -e ""
echo -e "4. View API docs:"
echo -e "   Visit: ${BLUE}${VERCEL_URL}/docs${NC}"
echo -e ""

echo -e "${GREEN}Deployment setup complete!${NC}\n"
