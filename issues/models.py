
from abc import ABC, abstractmethod


class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return dict(self.__dict__)


class Reporter(BaseEntity):
    def __init__(self, id, name, email, team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name cannot be empty")

        if not isinstance(self.email, str) or "@" not in self.email:
            raise ValueError("Invalid email")

        if not isinstance(self.team, str) or not self.team.strip():
            raise ValueError("Team cannot be empty")


class Issue(BaseEntity):
    ALLOWED_STATUSES = [
        "open",
        "in_progress",
        "resolved",
        "closed",
    ]

    ALLOWED_PRIORITIES = [
        "low",
        "medium",
        "high",
        "critical",
    ]

    def __init__(
        self, id, title, description, status,
        priority, reporter_id, created_at=None
    ):
        from datetime import datetime

        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = created_at or str(datetime.now())

    def validate(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Title cannot be empty")

        if self.status not in self.ALLOWED_STATUSES:
            raise ValueError("Invalid status")

        if self.priority not in self.ALLOWED_PRIORITIES:
            raise ValueError("Invalid priority")

        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")

        if (
            isinstance(self.reporter_id, bool)
            or not isinstance(self.reporter_id, int)
            or self.reporter_id < 1
        ):
            raise ValueError("Invalid reporter_id")

    def describe(self):
        return f"{self.title} [{self.priority}]"


class CriticalIssue(Issue):
    def describe(self):
        return (
            f"[URGENT] {self.title} "
            "— needs immediate attention"
        )


class LowPriorityIssue(Issue):
    def describe(self):
        return (
            f"{self.title} "
            "— low priority, handle when free"
        )