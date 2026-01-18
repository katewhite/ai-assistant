import os
from pathlib import Path

# Granola cache path
GRANOLA_CACHE_PATH = Path.home() / "Library/Application Support/Granola/cache-v3.json"

# Notion config (get from environment variable)
# To use: export NOTION_API_KEY="your_key_here"
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if not NOTION_API_KEY:
    raise ValueError("NOTION_API_KEY environment variable is required")
NOTION_DATABASE_ID = "24394399495980dbaae5d60a00d17b27"

# Notion context database (for syncing context files)
# Set this to your Notion database ID for context files
NOTION_CONTEXT_DATABASE_ID = os.getenv("NOTION_CONTEXT_DATABASE_ID", "2ec94399495980a8ba6ec1cd2c238a96")

# User identification (for filtering personal meetings)
MY_USER_ID = "19b41bfc-e113-44f4-8541-49a63b0aadcf"

# Granola URL template
GRANOLA_NOTE_BASE_URL = "https://notes.granola.ai/d/"
