from __future__ import annotations


class Task:
    """Represents a task inside a project."""

    _next_id = 1

    def __init__(self, title: str, status: str = "todo", assigned_to: str = "", project_id: int | None = None) -> None:
        self._title = title
        self._status = status
        self._assigned_to = assigned_to
        self._project_id = project_id
        self._id = Task._next_id
        Task._next_id += 1

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not value:
            raise ValueError("Title must not be empty")
        self._title = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        self._status = value

    @property
    def assigned_to(self) -> str:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: str) -> None:
        self._assigned_to = value

    @property
    def project_id(self) -> int | None:
        return self._project_id

    @classmethod
    def create(cls, title: str, status: str = "todo", assigned_to: str = "", project_id: int | None = None) -> "Task":
        return cls(title=title, status=status, assigned_to=assigned_to, project_id=project_id)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task = cls(title=data["title"], status=data.get("status", "todo"), assigned_to=data.get("assigned_to", ""), project_id=data.get("project_id"))
        task._id = data["id"]
        return task

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "status": self.status, "assigned_to": self.assigned_to, "project_id": self.project_id}

    def __str__(self) -> str:
        return f"Task(id={self.id}, title={self.title}, status={self.status})"
