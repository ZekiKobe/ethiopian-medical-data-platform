import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramImageDownloader:
    def __init__(self):
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)
        
    async def download_channel_images(self, channel_name, limit=100):
        try:
            await self.client.start()
            channel = await self.client.get_entity(channel_name)
            
            today = datetime.now().strftime('%Y-%m-%d')
            save_dir = os.path.join('data', 'raw', 'telegram_images', today, channel_name.replace('/', '_'))
            os.makedirs(save_dir, exist_ok=True)
            
            image_count = 0
            async for message in self.client.iter_messages(channel, limit=limit):
                if message.media:
                    try:
                        file_path = os.path.join(save_dir, f"{message.id}")
                        await message.download_media(file=file_path)
                        
                        # Log image metadata
                        metadata = {
                            'message_id': message.id,
                            'channel': channel_name,
                            'date': message.date.isoformat(),
                            'file_path': f"{file_path}.jpg"  # Assuming JPG for simplicity
                        }
                        
                        with open(f"{file_path}.json", 'w') as f:
                            json.dump(metadata, f)
                            
                        image_count += 1
                        logger.info(f"Downloaded image {image_count}/{limit} from {channel_name}")
                        
                    except Exception as e:
                        logger.error(f"Error downloading media from message {message.id}: {str(e)}")
            
            logger.info(f"Downloaded {image_count} images from {channel_name}")
            
        except Exception as e:
            logger.error(f"Error processing {channel_name}: {str(e)}")

async def main():
    downloader = TelegramImageDownloader()
    
    channels = [
        'chemed',
        'lobelia4cosmetics'
    ]
    
    for channel in channels:
        await downloader.download_channel_images(channel, limit=50)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())