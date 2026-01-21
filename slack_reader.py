"""
Slack API reader for fetching messages from specific channels.
"""

import re
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime, timezone
from typing import List, Dict, Optional
from config import SLACK_BOT_TOKEN


def format_slack_error(e: SlackApiError) -> str:
    """
    Format a Slack API error with detailed scope information.
    
    Args:
        e: SlackApiError exception
        
    Returns:
        Formatted error message string
    """
    error_code = e.response.get('error', 'unknown_error')
    error_msg = f"❌ Slack API Error: {error_code}"
    
    # For missing_scope errors, show exactly what's needed
    if error_code == 'missing_scope':
        needed = e.response.get('needed', '')
        provided = e.response.get('provided', '')
        if needed:
            error_msg += f"\n   🔑 Missing scope: {needed}"
        if provided:
            error_msg += f"\n   ✅ Provided scopes: {provided}"
        error_msg += "\n   💡 Fix: Add the missing scope in your Slack app settings and reinstall the app."
    
    return error_msg


def get_slack_client():
    """Initialize and return a Slack WebClient."""
    if not SLACK_BOT_TOKEN:
        raise ValueError("SLACK_BOT_TOKEN environment variable is required. Add it to .env file or export it.")
    return WebClient(token=SLACK_BOT_TOKEN)


def get_channel_id(client: WebClient, channel_name: str) -> Optional[str]:
    """
    Get channel ID from channel name.

    Args:
        client: Slack WebClient instance
        channel_name: Channel name (with or without #)

    Returns:
        str: Channel ID or None if not found
    """
    channel_name = channel_name.lstrip('#')

    # If channel_name looks like an ID (starts with C), return as-is
    if channel_name.startswith('C'):
        return channel_name

    try:
        # Paginate through all channels to find the channel
        cursor = None
        while True:
            response = client.conversations_list(
                types="public_channel,private_channel",
                limit=1000,
                cursor=cursor
            )
            for channel in response["channels"]:
                if channel["name"] == channel_name:
                    return channel["id"]

            # Check for more pages
            cursor = response.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break

    except SlackApiError as e:
        print(format_slack_error(e))

    return None


def get_messages_in_range(
    channel_names: List[str],
    start_date: datetime,
    end_date: datetime,
    client: Optional[WebClient] = None
) -> List[Dict]:
    """
    Fetch messages from specified Slack channels within a date range.
    
    Args:
        channel_names: List of channel names (with or without #) or channel IDs
        start_date: Start datetime (inclusive)
        end_date: End datetime (inclusive)
        client: Optional Slack WebClient (will create one if not provided)
    
    Returns:
        List of message dicts with keys: channel, channel_name, timestamp, text, user, permalink
    """
    if client is None:
        client = get_slack_client()
    
    # Ensure dates are timezone-aware
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    if end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)
    
    # Convert to Unix timestamps
    start_ts = start_date.timestamp()
    end_ts = end_date.timestamp()
    
    all_messages = []
    
    for channel_name in channel_names:
        if not channel_name.strip():
            continue
            
        channel_id = get_channel_id(client, channel_name.strip())
        if not channel_id:
            print(f"⚠️  Warning: Channel '{channel_name}' not found, skipping...")
            continue
        
        try:
            # Fetch channel info for name
            channel_info = client.conversations_info(channel=channel_id)
            channel_display_name = channel_info["channel"]["name"]
            
            # Fetch messages
            messages = []
            cursor = None
            
            while True:
                try:
                    response = client.conversations_history(
                        channel=channel_id,
                        oldest=str(start_ts),
                        latest=str(end_ts),
                        cursor=cursor,
                        limit=200
                    )
                    
                    for msg in response["messages"]:
                        # Skip bot messages and thread replies (unless you want them)
                        if msg.get("subtype") in ["bot_message", "thread_broadcast"]:
                            continue
                        
                        msg_ts = float(msg["ts"])
                        msg_dt = datetime.fromtimestamp(msg_ts, tz=timezone.utc)
                        
                        # Get user info
                        user_name = "Unknown"
                        if "user" in msg:
                            try:
                                user_info = client.users_info(user=msg["user"])
                                user_name = user_info["user"].get("real_name") or user_info["user"].get("name", "Unknown")
                            except:
                                user_name = msg.get("user", "Unknown")
                        
                        # Get permalink
                        try:
                            permalink_response = client.chat_getPermalink(
                                channel=channel_id,
                                message_ts=msg["ts"]
                            )
                            permalink = permalink_response["permalink"]
                        except:
                            permalink = f"https://app.slack.com/client/{client.team_id}/{channel_id}/p{msg['ts'].replace('.', '')}"
                        
                        messages.append({
                            "channel": channel_id,
                            "channel_name": channel_display_name,
                            "timestamp": msg_dt.strftime("%Y-%m-%d %H:%M:%S"),
                            "text": msg.get("text", ""),
                            "user": user_name,
                            "permalink": permalink
                        })
                    
                    # Check if there are more messages
                    if not response.get("has_more"):
                        break
                    cursor = response.get("response_metadata", {}).get("next_cursor")
                    if not cursor:
                        break
                        
                except SlackApiError as e:
                    print(f"Error fetching messages from {channel_display_name}:")
                    print(format_slack_error(e))
                    break
            
            all_messages.extend(messages)
            print(f"   Found {len(messages)} messages in #{channel_display_name}")
            
        except SlackApiError as e:
            print(f"Error accessing channel '{channel_name}':")
            print(format_slack_error(e))
            continue
    
    # Sort by timestamp (oldest first)
    all_messages.sort(key=lambda x: x["timestamp"])
    
    return all_messages


def send_dm_to_user(client: WebClient, user_id: str, message: str) -> bool:
    """
    Send a direct message to a user.
    
    Args:
        client: Slack WebClient instance
        user_id: User ID to send message to
        message: Message text to send
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Open a DM conversation with the user
        response = client.conversations_open(users=[user_id])
        channel_id = response["channel"]["id"]
        
        # Send the message
        client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        return True
    except SlackApiError as e:
        print("Error sending DM:")
        print(format_slack_error(e))
        return False


def get_user_id_by_email(client: WebClient, email: str) -> Optional[str]:
    """
    Get user ID from email address.
    
    Args:
        client: Slack WebClient instance
        email: Email address of the user
    
    Returns:
        str: User ID or None if not found
    """
    try:
        response = client.users_lookupByEmail(email=email)
        return response["user"]["id"]
    except SlackApiError:
        return None


def get_dm_messages_in_range(
    start_date: datetime,
    end_date: datetime,
    user_email: str,
    client: Optional[WebClient] = None
) -> List[Dict]:
    """
    Fetch all direct messages for the user within a date range.
    
    Args:
        start_date: Start datetime (inclusive)
        end_date: End datetime (inclusive)
        user_email: Email address of the user to fetch DMs for
        client: Optional Slack WebClient (will create one if not provided)
    
    Returns:
        List of message dicts with keys: channel, channel_name, timestamp, text, user, permalink
    """
    if client is None:
        client = get_slack_client()
    
    # Ensure dates are timezone-aware
    if start_date.tzinfo is None:
        start_date = start_date.replace(tzinfo=timezone.utc)
    if end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)
    
    # Convert to Unix timestamps
    start_ts = start_date.timestamp()
    end_ts = end_date.timestamp()
    
    # Get user ID
    user_id = get_user_id_by_email(client, user_email)
    if not user_id:
        print(f"⚠️  Warning: Could not find user ID for {user_email}, skipping DMs...")
        return []
    
    all_messages = []
    
    try:
        # Get all DM conversations
        cursor = None
        while True:
            response = client.conversations_list(
                types="im",
                limit=1000,
                cursor=cursor
            )
            
            for conversation in response["channels"]:
                dm_channel_id = conversation["id"]
                
                # Get the other user's info
                other_user_id = conversation.get("user")
                if not other_user_id:
                    continue
                
                try:
                    user_info = client.users_info(user=other_user_id)
                    other_user_name = user_info["user"].get("real_name") or user_info["user"].get("name", "Unknown")
                except:
                    other_user_name = "Unknown"
                
                # Fetch messages from this DM
                messages = []
                msg_cursor = None
                
                while True:
                    try:
                        msg_response = client.conversations_history(
                            channel=dm_channel_id,
                            oldest=str(start_ts),
                            latest=str(end_ts),
                            cursor=msg_cursor,
                            limit=200
                        )
                        
                        for msg in msg_response["messages"]:
                            # Skip bot messages
                            if msg.get("subtype") in ["bot_message", "thread_broadcast"]:
                                continue
                            
                            msg_ts = float(msg["ts"])
                            msg_dt = datetime.fromtimestamp(msg_ts, tz=timezone.utc)
                            
                            # Get sender info
                            sender_name = "Unknown"
                            if "user" in msg:
                                try:
                                    sender_info = client.users_info(user=msg["user"])
                                    sender_name = sender_info["user"].get("real_name") or sender_info["user"].get("name", "Unknown")
                                except:
                                    sender_name = msg.get("user", "Unknown")
                            
                            # Get permalink
                            try:
                                permalink_response = client.chat_getPermalink(
                                    channel=dm_channel_id,
                                    message_ts=msg["ts"]
                                )
                                permalink = permalink_response["permalink"]
                            except:
                                permalink = f"https://app.slack.com/client/{client.team_id}/{dm_channel_id}/p{msg['ts'].replace('.', '')}"
                            
                            messages.append({
                                "channel": dm_channel_id,
                                "channel_name": f"DM with {other_user_name}",
                                "timestamp": msg_dt.strftime("%Y-%m-%d %H:%M:%S"),
                                "text": msg.get("text", ""),
                                "user": sender_name,
                                "permalink": permalink
                            })
                        
                        # Check if there are more messages
                        if not msg_response.get("has_more"):
                            break
                        msg_cursor = msg_response.get("response_metadata", {}).get("next_cursor")
                        if not msg_cursor:
                            break
                            
                    except SlackApiError as e:
                        print(f"Error fetching messages from DM with {other_user_name}:")
                        print(format_slack_error(e))
                        break
                
                all_messages.extend(messages)
                if messages:
                    print(f"   Found {len(messages)} messages in DM with {other_user_name}")
            
            # Check if there are more conversations
            cursor = response.get("response_metadata", {}).get("next_cursor")
            if not cursor:
                break
                
    except SlackApiError as e:
        print("Error fetching DM conversations:")
        print(format_slack_error(e))
    
    # Sort by timestamp (oldest first)
    all_messages.sort(key=lambda x: x["timestamp"])
    
    return all_messages


def filter_gratitacos_by_recipients(
    messages: List[Dict],
    client: Optional[WebClient] = None
) -> List[Dict]:
    """
    Filter gratitacos messages to only include those where Kate, Hannah, or Jerica are recipients.
    
    Args:
        messages: List of message dicts from #gratitacos channel
        client: Optional Slack WebClient (will create one if not provided)
    
    Returns:
        Filtered list of messages
    """
    if client is None:
        client = get_slack_client()
    
    # Get user IDs for Kate, Hannah, and Jerica
    target_users = {
        "kate@intelligems.io": "Kate",
        "hannah@intelligems.io": "Hannah",  # Update with actual emails if different
        "jerica@intelligems.io": "Jerica"   # Update with actual emails if different
    }
    
    target_user_ids = {}
    target_names = set(["Kate", "Hannah", "Jerica"])
    
    for email, name in target_users.items():
        user_id = get_user_id_by_email(client, email)
        if user_id:
            target_user_ids[user_id] = name
    
    filtered = []
    
    for msg in messages:
        text = msg.get("text", "").lower()
        
        # Check for @mentions (user IDs in format <@U123456>)
        user_mentions = re.findall(r'<@([A-Z0-9]+)>', msg.get("text", ""))
        
        # Check if any target user is mentioned
        is_recipient = False
        for mention_id in user_mentions:
            if mention_id in target_user_ids:
                is_recipient = True
                break
        
        # Also check for name mentions in text (case-insensitive)
        if not is_recipient:
            for name in target_names:
                if name.lower() in text:
                    # Check if it's a taco sent TO them (not BY them)
                    # Look for patterns like "taco to @kate" or "taco for kate"
                    if any(pattern in text for pattern in [f"to {name.lower()}", f"for {name.lower()}", f"@{name.lower()}"]):
                        is_recipient = True
                        break
        
        if is_recipient:
            filtered.append(msg)
    
    return filtered


def get_slack_messages_for_week(
    start_date: datetime,
    end_date: datetime,
    user_email: str,
    channel_names: List[str],
    client: Optional[WebClient] = None
) -> List[Dict]:
    """
    Main function to fetch all Slack messages for the week.
    Fetches from specified channels, DMs, and filters gratitacos.
    
    Args:
        start_date: Start datetime (inclusive)
        end_date: End datetime (inclusive)
        user_email: Email address of the user
        channel_names: List of channel names to fetch from
        client: Optional Slack WebClient (will create one if not provided)
    
    Returns:
        Combined, sorted list of all messages
    """
    if client is None:
        client = get_slack_client()
    
    all_messages = []
    
    # Fetch from channels (excluding gratitacos for now)
    regular_channels = [ch for ch in channel_names if ch != "gratitacos"]
    if regular_channels:
        print("📱 Fetching messages from channels...")
        channel_messages = get_messages_in_range(regular_channels, start_date, end_date, client)
        all_messages.extend(channel_messages)
    
    # Fetch gratitacos and filter
    if "gratitacos" in channel_names:
        print("📱 Fetching messages from #gratitacos...")
        gratitacos_messages = get_messages_in_range(["gratitacos"], start_date, end_date, client)
        filtered_gratitacos = filter_gratitacos_by_recipients(gratitacos_messages, client)
        all_messages.extend(filtered_gratitacos)
        print(f"   Filtered to {len(filtered_gratitacos)} messages (tacos to Kate, Hannah, or Jerica)")
    
    # Fetch DMs
    print("📱 Fetching direct messages...")
    dm_messages = get_dm_messages_in_range(start_date, end_date, user_email, client)
    all_messages.extend(dm_messages)
    
    # Sort all messages by timestamp (oldest first)
    all_messages.sort(key=lambda x: x["timestamp"])
    
    print(f"   Total Slack messages: {len(all_messages)}")
    
    return all_messages
