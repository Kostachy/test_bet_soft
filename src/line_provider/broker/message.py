from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, kw_only=True)
class Message:
    message_id: UUID
    data: dict[str, Any]
    message_type: str = "message"
