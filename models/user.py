from __future__ import annotations


class Person:
    """Base class for people in the application."""

    def __init__(self, name: str, email: str = "") -> None:
        self._name = name
        self._email = email

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value:
            raise ValueError("Name must not be empty")
        self._name = value

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        self._email = value

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class User(Person):
    """Represents an application user who can own many projects."""

    _next_id = 1

    def __init__(self, name: str, email: str = "") -> None:
        super().__init__(name=name, email=email)
        self._id = User._next_id
        User._next_id += 1

    @property
    def id(self) -> int:
        return self._id

    @classmethod
    def create(cls, name: str, email: str = "") -> "User":
        return cls(name=name, email=email)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(name=data["name"], email=data.get("email", ""))
        user._id = data["id"]
        return user

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}

    def __str__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"
