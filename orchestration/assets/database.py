from dagster import asset, Output
from scripts.database.load_raw_data import load_messages_to_db

@asset(deps=["scrape_telegram_data"])
def load_raw_data():
    """Load scraped data into PostgreSQL"""
    result = load_messages_to_db()
    return Output(
        result,
        metadata={"tables_loaded": ["telegram_messages", "telegram_images"]}
    )