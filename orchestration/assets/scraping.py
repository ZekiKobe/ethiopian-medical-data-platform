from dagster import asset, Output
from typing import List
import asyncio
from scripts.scraping.telegram_scraper import TelegramScraper

@asset
def scrape_telegram_data() -> List[str]:
    """Scrape data from Telegram channels"""
    scraper = TelegramScraper()
    channels = ['chemed', 'lobelia4cosmetics', 'tikvahpharma']
    
    async def scrape_all():
        results = []
        for channel in channels:
            messages = await scraper.scrape_channel(channel)
            scraper.save_messages(messages, channel)
            results.append(f"{channel}: {len(messages)} messages")
        return results
    
    results = asyncio.run(scrape_all())
    return Output(results, metadata={"channels": channels})