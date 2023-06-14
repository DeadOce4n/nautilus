from dataclasses import dataclass


@dataclass
class User:
    id: int
    streamer_username: str
    streamer_password: str
    display_name: str
    comments: str
    is_active: bool
    enforce_schedule: bool
    reactivate_at: int
    schedule_items: list[str]
    art: str
    art_updated_at: int
    has_custom_art: bool
    links: dict[str, str]
