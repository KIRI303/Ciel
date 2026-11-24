import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path

# Ciel's permanent storage location
DATA_DIR = Path.home() / "CielData"
MEMORY_DIR = DATA_DIR / "memory"
DATABASE = MEMORY_DIR / "ciel.db"


def get_connection():
    """Connect to Ciel's memory database."""

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create Ciel's memory table if it doesn't exist."""

    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL
            )
        """)


def save_memory(content: str):
    """Save a new memory."""

    with get_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO memories (content, created_at)
            VALUES (?, ?)
            """,
            (content, datetime.now().isoformat(timespec="seconds")),
        )


def load_memories():
    """Retrieve all saved memories."""

    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM memories ORDER BY id").fetchall()

        return [dict(row) for row in rows]


def delete_memory(memory_id: int):
    """Delete a memory using its ID."""

    with get_connection() as connection:
        connection.execute("DELETE FROM memories WHERE id = ?", (memory_id,))


def save_message(role: str, message: str):
    """Save a message and automatically index it."""

    conversations_dir = DATA_DIR / "conversations"
    conversations_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat(timespec="seconds")

    # Save the message to the daily conversation archive
    today = datetime.now().strftime("%Y-%m-%d")
    conversation_file = conversations_dir / f"{today}.jsonl"

    entry = {
        "timestamp": timestamp,
        "role": role,
        "message": message,
    }

    with conversation_file.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Automatically add the message to the search index
    initialize_search()
    index_message(role, message, timestamp)


def initialize_search():
    """Create a full-text search index for conversations."""

    with get_connection() as connection:
        connection.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS conversation_search
            USING fts5(
                role,
                message,
                timestamp
            )
        """)


def index_message(role: str, message: str, timestamp: str):
    """Add a conversation message to the search index."""

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO conversation_search
            (role, message, timestamp)
            VALUES (?, ?, ?)
        """,
            (role, message, timestamp),
        )


def search_conversations(query: str, limit: int = 10):
    """Search previous conversations using natural-language keywords."""

    # Extract individual words and ignore punctuation
    tokens = re.findall(r"\w+", query.lower())

    # Nothing useful to search for
    if not tokens:
        return []

    # Convert words into a safe FTS5 query
    fts_query = " OR ".join(f'"{token}"' for token in tokens)

    with get_connection() as connection:
        results = connection.execute(
            """
            SELECT role, message, timestamp
            FROM conversation_search
            WHERE conversation_search MATCH ?
            ORDER BY rank
            LIMIT ?
            """,
            (fts_query, limit),
        ).fetchall()

        return [dict(row) for row in results]


def import_conversations():
    """Import existing JSONL archives into the search index."""

    conversations_dir = DATA_DIR / "conversations"
    conversations_dir.mkdir(parents=True, exist_ok=True)

    initialize_search()
    imported = 0

    with get_connection() as connection:
        for file_path in conversations_dir.glob("*.jsonl"):
            with file_path.open("r", encoding="utf-8") as file:
                for line in file:
                    if not line.strip():
                        continue

                    entry = json.loads(line)

                    # Check whether this message is already indexed
                    existing = connection.execute(
                        """
                        SELECT 1 FROM conversation_search
                        WHERE role = ? AND message = ? AND timestamp = ?
                        LIMIT 1
                        """,
                        (
                            entry["role"],
                            entry["message"],
                            entry["timestamp"],
                        ),
                    ).fetchone()

                    if existing is None:
                        connection.execute(
                            """
                            INSERT INTO conversation_search
                            (role, message, timestamp)
                            VALUES (?, ?, ?)
                            """,
                            (
                                entry["role"],
                                entry["message"],
                                entry["timestamp"],
                            ),
                        )

                        imported += 1

    return imported
