# Project Management CLI

A small command-line tool for managing users, projects, and tasks with JSON persistence and a built-in project summary feature.

## Features
- Add and list users, projects, and tasks
- Link tasks to projects and projects to users
- Mark tasks complete
- Generate a project summary using a reusable AI-style client module

## File Structure
- main.py: CLI entry point and command routing
- models/: domain classes for User, Project, and Task
- services/: JSON storage and summary client modules
- utils/: output formatting helpers
- data/: default persistence location
- tests/: CLI regression tests

## Setup
1. Create and activate a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the CLI:
   ```bash
   python main.py add-user --name "Alex" --email "alex@example.com"
   ```

## Example Commands
```bash
python main.py add-user --name "Alex" --email "alex@example.com"
python main.py add-project --user "Alex" --title "CLI Tool" --description "Build a management CLI"
python main.py add-task --project "CLI Tool" --title "Implement add-task"
python main.py summarize-project --project "CLI Tool"
```

## External Summary Feature
The summary feature uses the reusable AI client module in services/ai_client.py. It currently generates a deterministic project summary from stored task data and gracefully returns an error message if something goes wrong.

## Notes
- Data is stored in JSON at data/project_data.json by default.
- The environment variable PROJECT_DATA_FILE can override the storage location.
