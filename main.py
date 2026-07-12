import os
from pathlib import Path

from rich.console import Console

from models.user import User
from models.project import Project
from models.task import Task
from services.storage_service import StorageService
from services.ai_client import AIClient
from utils.formatters import format_project_summary


DEFAULT_DATA_FILE = Path(os.getenv("PROJECT_DATA_FILE", Path(__file__).parent / "data" / "project_data.json"))
console = Console()


def sync_ids(app: dict) -> None:
    """Keep class-level ID counters aligned with persisted data."""
    users = app.get("users", [])
    projects = app.get("projects", [])
    tasks = app.get("tasks", [])
    User._next_id = max((user["id"] for user in users), default=0) + 1
    Project._next_id = max((project["id"] for project in projects), default=0) + 1
    Task._next_id = max((task["id"] for task in tasks), default=0) + 1


def build_parser():
    import argparse

    parser = argparse.ArgumentParser(description="Project management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_user = subparsers.add_parser("add-user", help="Add a new user")
    add_user.add_argument("--name", required=True)
    add_user.add_argument("--email", required=True)

    add_project = subparsers.add_parser("add-project", help="Add a project for a user")
    add_project.add_argument("--user", required=True)
    add_project.add_argument("--title", required=True)
    add_project.add_argument("--description", default="")
    add_project.add_argument("--due-date", dest="due_date", default="")

    add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    add_task.add_argument("--project", required=True)
    add_task.add_argument("--title", required=True)
    add_task.add_argument("--status", default="todo")
    add_task.add_argument("--assigned-to", dest="assigned_to", default="")

    list_users = subparsers.add_parser("list-users", help="List all users")
    list_projects = subparsers.add_parser("list-projects", help="List all projects")
    list_tasks = subparsers.add_parser("list-tasks", help="List all tasks")

    complete_task = subparsers.add_parser("complete-task", help="Mark a task as complete")
    complete_task.add_argument("--project", required=True)
    complete_task.add_argument("--title", required=True)

    summarize_project = subparsers.add_parser("summarize-project", help="Generate a summary for a project")
    summarize_project.add_argument("--project", required=True)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    storage = StorageService(DEFAULT_DATA_FILE)
    app = storage.load()
    if app is None:
        app = {"users": [], "projects": [], "tasks": []}

    sync_ids(app)

    if args.command == "add-user":
        user = User.create(name=args.name, email=args.email)
        app["users"].append(user.to_dict())
        storage.save(app)
        console.print(f"[green]Added user:[/green] {user}")
        return

    if args.command == "add-project":
        user = next((u for u in app["users"] if u.get("name") == args.user), None)
        if user is None:
            console.print(f"[red]User '{args.user}' not found.[/red]")
            return
        project = Project.create(title=args.title, description=args.description, due_date=args.due_date, user_id=user["id"])
        app["projects"].append(project.to_dict())
        storage.save(app)
        console.print(f"[green]Added project:[/green] {project}")
        return

    if args.command == "add-task":
        project = next((p for p in app["projects"] if p.get("title") == args.project), None)
        if project is None:
            console.print(f"[red]Project '{args.project}' not found.[/red]")
            return
        task = Task.create(title=args.title, status=args.status, assigned_to=args.assigned_to, project_id=project["id"])
        app["tasks"].append(task.to_dict())
        storage.save(app)
        console.print(f"[green]Added task:[/green] {task}")
        return

    if args.command == "list-users":
        for user in app["users"]:
            console.print(User.from_dict(user))
        return

    if args.command == "list-projects":
        for project in app["projects"]:
            console.print(Project.from_dict(project))
        return

    if args.command == "list-tasks":
        for task in app["tasks"]:
            console.print(Task.from_dict(task))
        return

    if args.command == "complete-task":
        task = next((t for t in app["tasks"] if t.get("title") == args.title and t.get("project_id") == next((p["id"] for p in app["projects"] if p.get("title") == args.project), None)), None)
        if task is None:
            console.print("[red]Task not found.[/red]")
            return
        task["status"] = "done"
        storage.save(app)
        console.print(f"[green]Completed task:[/green] {task['title']}")
        return

    if args.command == "summarize-project":
        project = next((p for p in app["projects"] if p.get("title") == args.project), None)
        if project is None:
            console.print(f"[red]Project '{args.project}' not found.[/red]")
            return
        project_tasks = [task for task in app["tasks"] if task.get("project_id") == project["id"]]
        client = AIClient()
        summary = client.summarize_project(project, project_tasks)
        console.print(format_project_summary(project, project_tasks, summary))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
