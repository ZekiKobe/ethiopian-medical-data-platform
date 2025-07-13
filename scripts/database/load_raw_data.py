import os
import json
import psycopg2
from dotenv import load_dotenv
from datetime import datetime
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )

def create_raw_schema(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE SCHEMA IF NOT EXISTS raw;
        
        CREATE TABLE IF NOT EXISTS raw.telegram_messages (
            id BIGINT PRIMARY KEY,
            date TIMESTAMP WITH TIME ZONE,
            message TEXT,
            views INTEGER,
            media JSONB,
            channel VARCHAR(255),
            scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS raw.telegram_images (
            message_id BIGINT,
            channel VARCHAR(255),
            date TIMESTAMP WITH TIME ZONE,
            file_path TEXT,
            scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (message_id, channel)
        );
        """)
        conn.commit()
    logger.info("Created raw schema and tables")

def load_messages_to_db(conn):
    messages_dir = os.path.join('data', 'raw', 'telegram_messages')
    loaded_files = set()
    
    # Check already loaded files
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT channel, date FROM raw.telegram_messages")
        loaded_records = cur.fetchall()
        loaded_files = {(rec[0], datetime.fromisoformat(rec[1]).date()) for rec in loaded_records}
    
    for root, _, files in os.walk(messages_dir):
        for file in files:
            if file.endswith('.json'):
                channel_name = file.replace('.json', '').replace('_', '/')
                file_date = datetime.strptime(root.split(os.sep)[-1], '%Y-%m-%d').date()
                
                if (channel_name, file_date) in loaded_files:
                    logger.info(f"Skipping already loaded {channel_name} for {file_date}")
                    continue
                
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                
                with conn.cursor() as cur:
                    for msg in messages:
                        cur.execute("""
                        INSERT INTO raw.telegram_messages (id, date, message, views, media, channel)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                        """, (
                            msg['id'],
                            msg['date'],
                            msg['message'],
                            msg['views'],
                            json.dumps(msg['media']) if msg['media'] else None,
                            msg['channel']
                        ))
                    conn.commit()
                logger.info(f"Loaded {len(messages)} messages from {file_path}")

def load_images_metadata_to_db(conn):
    images_dir = os.path.join('data', 'raw', 'telegram_images')
    
    for root, _, files in os.walk(images_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    metadata = json.load(f)
                
                with conn.cursor() as cur:
                    cur.execute("""
                    INSERT INTO raw.telegram_images (message_id, channel, date, file_path)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (message_id, channel) DO NOTHING
                    """, (
                        metadata['message_id'],
                        metadata['channel'],
                        metadata['date'],
                        metadata['file_path']
                    ))
                    conn.commit()
                logger.info(f"Loaded image metadata from {file_path}")

if __name__ == '__main__':
    conn = get_db_connection()
    try:
        create_raw_schema(conn)
        load_messages_to_db(conn)
        load_images_metadata_to_db(conn)
    finally:
        conn.close()