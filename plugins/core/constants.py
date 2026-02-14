"""
Constants and enums used throughout the bot
"""

from enum import Enum, auto
from typing import Dict, List


class TaskStatus(Enum):
    """Task status enum"""
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    ERROR = "error"
    SKIPPED = "skipped"


class FileType(Enum):
    """File type enum"""
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    PHOTO = "photo"
    ANIMATION = "animation"
    STICKER = "sticker"
    VOICE = "voice"
    TEXT = "text"
    POLL = "poll"
    LOCATION = "location"
    CONTACT = "contact"
    UNKNOWN = "unknown"


class MessageType(Enum):
    """Message type enum"""
    PRIVATE = "private"
    PUBLIC = "public"
    BOT = "bot"
    JOIN_CHAT = "join_chat"


# File extensions mapping
FILE_EXTENSIONS: Dict[FileType, str] = {
    FileType.PHOTO: ".jpg",
    FileType.VIDEO: ".mp4",
    FileType.AUDIO: ".mp3",
    FileType.ANIMATION: ".mp4",
    FileType.VOICE: ".ogg",
    FileType.STICKER: ".webp",
    FileType.TEXT: ".txt",
    FileType.DOCUMENT: "",
}

# Special file extensions based on MIME type
MIME_EXTENSIONS: Dict[str, str] = {
    "image/gif": ".gif",
    "video/x-matroska": ".mkv",
    "video/webm": ".webm",
    "audio/ogg": ".ogg",
    "audio/wav": ".wav",
    "audio/mpeg": ".mp3",
    "image/webp": ".webp",
    "application/x-tgsticker": ".tgs",
}

# Allowed file types for download
ALLOWED_FILE_TYPES: List[str] = [
    "document", "video", "audio", "photo", "animation", "sticker", "voice", "text"
]

# Maximum file size per type (in MB)
MAX_FILE_SIZE_BY_TYPE: Dict[str, int] = {
    "document": 2000,
    "video": 2000,
    "audio": 2000,
    "photo": 10,
    "animation": 50,
    "sticker": 1,
    "voice": 50,
}

# Progress bar styles
PROGRESS_STYLES: List[str] = ["gradient", "block", "circle", "square", "arrow", "modern"]

# Spinner frames for animations
SPINNER_FRAMES: Dict[str, List[str]] = {
    "downloading": ["⡀", "⡄", "⡆", "⡇", "⡏", "⡟", "⡿", "⣿", "⣷", "⣯", "⣟", "⣿"],
    "uploading": ["⬆️", "↗️", "➡️", "↘️", "⬇️", "↙️", "⬅️", "↖️"],
    "processing": ["⚙️", "🔧", "🛠️", "🔨"],
    "waiting": ["⏳", "⌛", "⏰", "🕐", "🕑", "🕒", "🕓", "🕔"],
    "success": ["✅", "✨", "🎉", "🔥", "🌟", "💫"],
    "error": ["❌", "⚠️", "🚫", "💥"],
}

# Progress bar characters
PROGRESS_BAR_CHARS: Dict[str, List[str]] = {
    "gradient": ["░", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"],
    "block": ["□", "░", "▒", "▓", "█"],
    "circle": ["○", "◔", "◑", "◕", "●"],
    "square": ["□", "◱", "◲", "■"],
    "arrow": ["-", "▸", "▹", "►", "▻", "▶"],
    "modern": ["⣀", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"],
}

# File icons
FILE_ICONS: Dict[str, str] = {
    "video": "🎬",
    "audio": "🎵",
    "document": "📄",
    "photo": "🖼️",
    "animation": "🎞️",
    "sticker": "🏷️",
    "voice": "🎤",
    "text": "📝",
    "zip": "📦",
    "archive": "🗜️",
    "executable": "⚙️",
    "code": "💻",
    "pdf": "📕",
    "unknown": "📁",
}

# Status emojis
STATUS_EMOJIS: Dict[str, str] = {
    "downloading": "⬇️",
    "uploading": "⬆️",
    "processing": "⚙️",
    "queued": "⏳",
    "completed": "✅",
    "paused": "⏸️",
    "cancelled": "🚫",
    "error": "❌",
}

# Speed emojis
SPEED_EMOJIS: Dict[str, str] = {
    "very_fast": "🚀",  # >10 MB/s
    "fast": "⚡",        # >1 MB/s
    "medium": "🐇",      # >100 KB/s
    "slow": "🚶",        # >10 KB/s
    "very_slow": "🐌",   # <10 KB/s
}

# Command descriptions for help menu
COMMAND_DESCRIPTIONS: Dict[str, str] = {
    "start": "Start the bot",
    "help": "Show help message",
    "login": "Login with phone number (for private content)",
    "logout": "Logout and clear session",
    "settings": "Configure bot settings",
    "cancel": "Cancel current operation",
    "stats": "Show bot statistics (admin only)",
    "users": "Show user list (admin only)",
    "backup": "Create database backup (admin only)",
    "broadcast": "Send message to all users (admin only)",
    "restart": "Restart the bot (admin only)",
}

# Error messages
ERROR_MESSAGES: Dict[str, str] = {
    "access_denied": "⛔ **Access Denied**\n\nYou are not authorized to use this bot.",
    "login_required": "🔐 **Login Required**\n\nFor downloading restricted content you have to /login first.",
    "session_expired": "❌ **Session Expired**\n\nYour login session has expired. Please /logout first then /login again.",
    "invalid_link": "❌ **Invalid Link Format**\n\nPlease provide a valid Telegram link.",
    "batch_active": "⏳ **One task is already processing. Please wait for it to complete.**\n\nUse /cancel to stop current operation.",
    "no_session": "❌ **String Session is not Set**\n\nPlease configure a string session in the bot settings.",
}

# Success messages
SUCCESS_MESSAGES: Dict[str, str] = {
    "chat_joined": "✅ Chat Joined",
    "already_joined": "✅ Chat already Joined",
    "cancelled": "✅ **Batch Successfully Cancelled.**\n\nAll operations have been stopped and resources freed.",
}