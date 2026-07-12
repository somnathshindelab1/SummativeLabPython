from __future__ import annotations

from typing import Any


class AIClient:
    """Provides a reusable summary service for project data."""

    def summarize_project(self, project: dict[str, Any], tasks: list[dict[str, Any]]) -> str:
        try:
            total_tasks = len(tasks)
            done_tasks = sum(1 for task in tasks if task.get("status") == "done")
            pending_tasks = total_tasks - done_tasks
            title = project.get("title", "Untitled")
            description = project.get("description", "") or "No description provided."
            return (
                f"Summary for '{title}': {description} "
                f"There are {total_tasks} tasks, {done_tasks} completed and {pending_tasks} still pending. "
                f"Suggested next step: focus on the highest-priority pending task."
            )
        except Exception as exc:
            return f"Unable to generate summary right now: {exc}"
