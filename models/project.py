from __future__ import annotations


class Project:
    """Represents a project owned by a user."""

    _next_id = 1

    def __init__(self, title: str, description: str = "", due_date: str = "", user_id: int | None = None) -> None:
        self._title = title
        self._description = description
        self._due_date = due_date
        self._user_id = user_id
        self._id = Project._next_id
        Project._next_id += 1

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
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def due_date(self) -> str:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str) -> None:
        self._due_date = value

    @property
    def user_id(self) -> int | None:
        return self._user_id

    @classmethod
    def create(cls, title: str, description: str = "", due_date: str = "", user_id: int | None = None) -> "Project":
        return cls(title=title, description=description, due_date=due_date, user_id=user_id)

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        project = cls(title=data["title"], description=data.get("description", ""), due_date=data.get("due_date", ""), user_id=data.get("user_id"))
        project._id = data["id"]
        return project

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "description": self.description, "due_date": self.due_date, "user_id": self.user_id}

    def __str__(self) -> str:
        return f"Project(id={self.id}, title={self.title}, due_date={self.due_date})"
