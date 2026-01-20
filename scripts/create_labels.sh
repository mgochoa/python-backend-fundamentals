#!/bin/bash

# Script to create GitHub labels for the Python Backend Learning Project
# Run this BEFORE create_github_issues.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Creating GitHub Labels ===${NC}"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed"
    exit 1
fi

# Create labels with colors
echo "Creating labels..."

# Difficulty levels
gh label create "beginner" --color "0E8A16" --description "Beginner level task" --force
gh label create "intermediate" --color "FBCA04" --description "Intermediate level task" --force
gh label create "advanced" --color "D93F0B" --description "Advanced level task" --force

# Task types
gh label create "setup" --color "1D76DB" --description "Project setup tasks" --force
gh label create "reference" --color "5319E7" --description "Study reference implementation" --force
gh label create "guided" --color "0052CC" --description "Guided implementation with TODOs" --force
gh label create "challenge" --color "C5DEF5" --description "Independent implementation" --force
gh label create "bonus" --color "FEF2C0" --description "Optional extensions" --force
gh label create "study" --color "BFD4F2" --description "Study and learning tasks" --force

# Technical areas
gh label create "crud" --color "D4C5F9" --description "CRUD operations" --force
gh label create "validation" --color "F9D0C4" --description "Data validation" --force
gh label create "relationships" --color "C2E0C6" --description "Database relationships" --force
gh label create "queries" --color "BFDADC" --description "SQL queries" --force
gh label create "business-logic" --color "FEF2C0" --description "Business logic implementation" --force
gh label create "design" --color "D876E3" --description "Design and architecture" --force
gh label create "interface" --color "E99695" --description "User interface" --force
gh label create "api" --color "F9D0C4" --description "API development" --force

echo ""
echo -e "${GREEN}✓ All labels created successfully!${NC}"
echo ""
echo "Now you can run: ./create_github_issues.sh"
