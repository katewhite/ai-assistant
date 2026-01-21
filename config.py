import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Granola cache path
GRANOLA_CACHE_PATH = Path.home() / "Library/Application Support/Granola/cache-v3.json"

# Notion config (get from environment variable or .env file)
# To use: export NOTION_API_KEY="your_key_here" or add to .env file
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if not NOTION_API_KEY:
    raise ValueError("NOTION_API_KEY environment variable is required. Add it to .env file or export it.")
NOTION_DATABASE_ID = "24394399495980dbaae5d60a00d17b27"

# Notion context database (for syncing context files)
# Set this to your Notion database ID for context files
NOTION_CONTEXT_DATABASE_ID = os.getenv("NOTION_CONTEXT_DATABASE_ID", "2ec94399495980a8ba6ec1cd2c238a96")

# Direct reports parent page ID
# Parent page: https://www.notion.so/Weekly-Direct-Reports-Notes-2ee94399495980fdae61e45a717281e9
DIRECT_REPORTS_PARENT_PAGE_ID = "2ee94399495980fdae61e45a717281e9"

# User identification (for filtering personal meetings)
MY_USER_ID = "19b41bfc-e113-44f4-8541-49a63b0aadcf"

# Granola URL template
GRANOLA_NOTE_BASE_URL = "https://notes.granola.ai/d/"

# Slack config (get from environment variable or .env file)
# To use: export SLACK_BOT_TOKEN="xoxb-your-token" or add to .env file
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
# Optional: specify which channels to monitor (comma-separated channel names or IDs)
# Default: empty list means you'll need to specify channels when calling the function
SLACK_CHANNELS = os.getenv("SLACK_CHANNELS", "pillar_core_experiences,product-announce").split(",") if os.getenv("SLACK_CHANNELS") else ["pillar_core_experiences", "product-announce"]
# User email for DM delivery (optional, can also use user ID)
SLACK_USER_EMAIL = os.getenv("SLACK_USER_EMAIL", "kate@intelligems.io")

# Weekly journaling Slack channels
WEEKLY_JOURNALING_SLACK_CHANNELS = [
    "pillar_core_experiences",
    "product-announce",
    "product-design-guild",
    "tech-team",
    "tech-team-leadership",
    "gratitacos",
    "deployment-summary"
]
