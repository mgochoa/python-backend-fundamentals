#!/bin/bash

# Script to create a GitHub Project board for the Python Backend Learning Project
# Run this AFTER create_github_issues.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== Creating GitHub Project Board ===${NC}"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed"
    exit 1
fi

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
OWNER=$(echo $REPO | cut -d'/' -f1)

echo -e "${BLUE}Repository: ${REPO}${NC}"
echo ""

# Create the project (Projects V2)
echo "Creating project board..."
PROJECT_ID=$(gh project create \
  --owner "$OWNER" \
  --title "Python Backend Learning Journey" \
  --format json 2>&1 | tee /tmp/gh_project_output.txt | jq -r '.id' 2>/dev/null)

if [ -z "$PROJECT_ID" ] || grep -q "missing required scopes" /tmp/gh_project_output.txt; then
    echo ""
    echo -e "${YELLOW}⚠ GitHub authentication needs project permissions${NC}"
    echo ""
    echo "Please run this command to add the required permissions:"
    echo -e "${BLUE}  gh auth refresh -s project,read:project${NC}"
    echo ""
    echo "Then run this script again: ./create_project.sh"
    exit 1
fi

echo -e "${GREEN}✓ Project created!${NC}"
echo ""

# Note: GitHub Projects V2 uses a different structure
# The default view has a "Status" field with: Todo, In Progress, Done
# We'll add issues to the project and they'll appear in the default view

echo -e "${YELLOW}Adding issues to project...${NC}"
echo ""

# Get all issues from the repository
ISSUE_NUMBERS=$(gh issue list --repo "$REPO" --limit 100 --json number --jq '.[].number')

# Add each issue to the project
for ISSUE_NUM in $ISSUE_NUMBERS; do
    gh project item-add "$PROJECT_ID" --owner "$OWNER" --url "https://github.com/$REPO/issues/$ISSUE_NUM" 2>/dev/null || true
    echo -e "${GREEN}✓ Added issue #${ISSUE_NUM}${NC}"
done

echo ""
echo -e "${BLUE}=== Project Setup Complete! ===${NC}"
echo ""
echo -e "${GREEN}✓ Project created: Python Backend Learning Journey${NC}"
echo -e "${GREEN}✓ All issues added to project${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. View your project: gh project view $PROJECT_ID --owner $OWNER --web"
echo "2. Organize issues by dragging them between columns"
echo "3. Use the Status field to track progress: Todo → In Progress → Done"
echo "4. Start with Story 1: Project Setup!"
echo ""
echo "Or open directly in browser:"
echo "https://github.com/users/$OWNER/projects"
echo ""
