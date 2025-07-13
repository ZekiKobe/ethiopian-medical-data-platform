import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TelegramScraper:
    def __init__(self):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)
        
    async def scrape_channel(self, channel_name, limit=1000):
        try:
            await self.client.start()
            channel = await self.client.get_entity(channel_name)
            
            all_messages = []
            offset_id = 0
            
            while True:
                history = await self.client(GetHistoryRequest(
                    peer=channel,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=min(100, limit),  # 100 is the max per request
                    max_id=0,
                    min_id=0,
                    hash=0
                ))
                
                if not history.messages:
                    break
                
                messages = history.messages
                for message in messages:
                    message_dict = {
                        'id': message.id,
                        'date': message.date.isoformat(),
                        'message': message.message,
                        'views': message.views if hasattr(message, 'views') else None,
                        'media': self._process_media(message.media) if message.media else None,
                        'channel': channel_name
                    }
                    all_messages.append(message_dict)
                
                offset_id = messages[-1].id
                limit -= len(messages)
                if limit <= 0:
                    break
            
            return all_messages
        except Exception as e:
            logger.error(f"Error scraping {channel_name}: {str(e)}")
            return []

    def _process_media(self, media):
        media_info = {
            'type': str(media.__class__.__name__),
            'size': getattr(media, 'size', None),
            'mime_type': getattr(media, 'mime_type', None)
        }
        
        if hasattr(media, 'photo'):
            media_info['photo_id'] = media.photo.id
        if hasattr(media, 'document'):
            media_info['document_id'] = media.document.id
            
        return media_info

    def save_messages(self, messages, channel_name):
        if not messages:
            return
            
        today = datetime.now().strftime('%Y-%m-%d')
        save_dir = os.path.join('data', 'raw', 'telegram_messages', today)
        os.makedirs(save_dir, exist_ok=True)
        
        filename = f"{channel_name.replace('/', '_')}.json"
        filepath = os.path.join(save_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Saved {len(messages)} messages from {channel_name} to {filepath}")

async def main():
    scraper = TelegramScraper()
    
    channels = [
        'chemed',
        'lobelia4cosmetics',
        'tikvahpharma'
    ]
    
    for channel in channels:
        messages = await scraper.scrape_channel(channel, limit=1000)
        scraper.save_messages(messages, channel)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())