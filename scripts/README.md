# GitHub Setup Scripts

These scripts were used to set up the GitHub repository with issues and project board.

## Scripts

- `create_labels.sh` - Creates all GitHub labels
- `create_github_issues.sh` - Creates 18 issues from user stories
- `create_project.sh` - Creates GitHub Project board and adds issues
- `setup_github_project.sh` - Master script that runs all of the above

## Usage

These scripts have already been run. They're kept here for reference or if you need to recreate the setup in another repository.

To use in a new repository:
```bash
cd scripts
./setup_github_project.sh
```

## Requirements

- GitHub CLI (`gh`) installed and authenticated
- `jq` for JSON parsing (project creation)
- Project permissions: `gh auth refresh -s project,read:project`
