from typing import Any


def format_project_summary(project: dict[str, Any], tasks: list[dict[str, Any]], summary: str) -> str:
    """Format project details and a generated summary for CLI output."""
    task_lines = "\n".join(f"- {task['title']} [{task.get('status', 'todo')}]" for task in tasks) or "- No tasks yet"
    return (
        f"Project: {project.get('title', 'Untitled')}\n"
        f"Description: {project.get('description', '') or 'No description provided.'}\n"
        f"Due date: {project.get('due_date', 'Not set')}\n"
        f"Tasks:\n{task_lines}\n"
        f"Summary: {summary}"
    )
