#!/usr/bin/env python3
"""
Unified script to sync context from both Granola and Notion.
"""

import sys
from pathlib import Path

# Import sync scripts
try:
    from sync_granola_calls import main as sync_granola
except ImportError as e:
    print(f"Warning: Could not import sync_granola_calls: {e}")
    sync_granola = None

try:
    from sync_notion_context import main as sync_notion
except ImportError as e:
    print(f"Warning: Could not import sync_notion_context: {e}")
    sync_notion = None


def main():
    """Run both Granola and Notion syncs."""
    print("=" * 60)
    print("Syncing Context from All Sources")
    print("=" * 60)
    print()
    
    results = {}
    
    # Sync from Granola
    if sync_granola:
        print("📞 Syncing from Granola...")
        print("-" * 60)
        try:
            granola_result = sync_granola()
            results["granola"] = granola_result
        except Exception as e:
            print(f"❌ Error syncing from Granola: {e}")
            results["granola"] = 1
        print()
    else:
        print("⏭️  Skipping Granola sync (module not available)")
        print()
        results["granola"] = None
    
    # Sync from Notion
    if sync_notion:
        print("📝 Syncing from Notion...")
        print("-" * 60)
        try:
            notion_result = sync_notion()
            results["notion"] = notion_result
        except Exception as e:
            print(f"❌ Error syncing from Notion: {e}")
            results["notion"] = 1
        print()
    else:
        print("⏭️  Skipping Notion sync (module not available)")
        print()
        results["notion"] = None
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    if results.get("granola") is not None:
        status = "✅ Success" if results["granola"] == 0 else "❌ Failed"
        print(f"Granola: {status}")
    
    if results.get("notion") is not None:
        status = "✅ Success" if results["notion"] == 0 else "❌ Failed"
        print(f"Notion:  {status}")
    
    # Return error code if any sync failed
    has_errors = any(
        result is not None and result != 0
        for result in results.values()
    )
    
    return 1 if has_errors else 0


if __name__ == "__main__":
    exit(main())
