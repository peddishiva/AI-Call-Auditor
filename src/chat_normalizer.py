import re
import json

class ChatNormalizer:
    def __init__(self):
        pass

    def normalize_content(self, raw_text):
        """
        Parses raw chat text into structured JSON.
        Supports standard timestamped formats.
        """
        lines = raw_text.strip().split('\n')
        structured_chat = []
        
        # Regex patterns for common formats
        # 1. [HH:MM:SS] Speaker: Message
        # 2. Speaker: Message
        pattern_timestamp = re.compile(r'\[(.*?)\]\s*([^:]+):\s*(.*)')
        pattern_simple = re.compile(r'([^:]+):\s*(.*)')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match_ts = pattern_timestamp.match(line)
            match_simple = pattern_simple.match(line)

            if match_ts:
                timestamp, speaker, message = match_ts.groups()
                structured_chat.append({
                    "timestamp": timestamp,
                    "speaker": speaker.strip(),
                    "text": message.strip()
                })
            elif match_simple:
                speaker, message = match_simple.groups()
                # Use simple index as timestamp logic placeholder or None
                structured_chat.append({
                    "timestamp": None,
                    "speaker": speaker.strip(),
                    "text": message.strip()
                })
            else:
                # Fallback for continuation lines or system messages
                structured_chat.append({
                    "timestamp": None,
                    "speaker": "System",
                    "text": line
                })
        
        return structured_chat

    def export_to_json(self, chat_data, output_path):
        with open(output_path, 'w') as f:
            json.dump(chat_data, f, indent=4)
        return output_path
