#!/bin/bash

# Master script to set up the complete GitHub project
# This runs all setup scripts in the correct order

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Python Backend Learning Project - GitHub Setup       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with GitHub CLI${NC}"
    echo "Run: gh auth login"
    exit 1
fi

# Check if jq is installed (needed for project creation)
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}Warning: jq is not installed. Project creation may fail.${NC}"
    echo "Install it with: brew install jq"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}"
echo ""

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo -e "${BLUE}Repository: ${REPO}${NC}"
echo ""

echo -e "${YELLOW}This will:${NC}"
echo "  1. Create all necessary labels"
echo "  2. Create 18 GitHub issues from user stories"
echo "  3. Create a GitHub Project board"
echo "  4. Add all issues to the project"
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${BLUE}═══ Step 1/3: Creating Labels ═══${NC}"
echo ""
./create_labels.sh

echo ""
echo -e "${BLUE}═══ Step 2/3: Creating Issues ═══${NC}"
echo ""
# Run create_github_issues.sh with auto-yes
echo "y" | ./create_github_issues.sh

echo ""
echo -e "${BLUE}═══ Step 3/3: Creating Project Board ═══${NC}"
echo ""
./create_project.sh

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✓ Setup Complete!                                     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}What's been created:${NC}"
echo "  ✓ 16 labels for organizing issues"
echo "  ✓ 18 issues with detailed user stories"
echo "  ✓ 1 project board with all issues"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. View your project: gh repo view --web"
echo "  2. Go to the Projects tab"
echo "  3. Start with Story 1: Project Setup"
echo ""
echo -e "${GREEN}Happy learning! 🚀${NC}"
echo ""
