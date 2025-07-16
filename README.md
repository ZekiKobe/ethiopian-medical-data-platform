# Ethiopian Medical Data Platform

![Pipeline Architecture](docs/architecture.png)

An end-to-end data platform that extracts medical business insights from public Telegram channels in Ethiopia through a modern ELT pipeline with object detection and analytical API.

## Table of Contents
- [Features](#-features)
- [Business Insights](#-business-insights)
- [Technical Stack](#-technical-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Task Details](#-task-details)
  - [Task 1: Data Scraping](#task-1-data-scraping)
  - [Task 2: Data Modeling](#task-2-data-modeling)
  - [Task 3: Object Detection](#task-3-object-detection)
  - [Task 4: Analytical API](#task-4-analytical-api)
  - [Task 5: Orchestration](#task-5-orchestration)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Features
- Telegram data scraping with Telethon
- Data lake with partitioned JSON storage
- Star schema data warehouse in PostgreSQL
- dbt transformations with testing
- YOLOv8 image object detection
- FastAPI analytical endpoints
- Dagster pipeline orchestration
- Dockerized environment

## 📊 Business Insights
Answers key questions:
1. Top 10 mentioned medical products
2. Price/availability across channels
3. Visual content analysis (pills vs creams)
4. Daily/weekly posting trends
5. Channel comparison metrics

## 🛠️ Technical Stack
| Component          | Technology               |
|--------------------|--------------------------|
| Data Extraction    | Telethon                 |
| Data Storage       | PostgreSQL 13            |
| Transformation     | dbt-core 1.10+           |
| Object Detection   | YOLOv8 (Ultralytics)     |
| API Framework      | FastAPI + Uvicorn        |
| Orchestration      | Dagster                  |
| Infrastructure     | Docker + Docker Compose  |

## 🏗️ Project Structure
.
├── data/ # Data storage
│ ├── raw/ # Raw JSON from Telegram
│ └── processed/ # Processed outputs
├── dbt/ # Transformation models
│ └── medical_analytics/ # dbt project
├── app/ # Application code
│ ├── api/ # FastAPI endpoints
│ └── object_detection/ # YOLO processing
├── orchestration/ # Dagster pipelines
├── scripts/ # Utility scripts
│ ├── scraping/ # Telegram scrapers
│ └── database/ # DB operations
├── docs/ # Documentation
├── docker-compose.yml # Service definitions
└── requirements.txt # Python dependencies

text

## 📦 Installation
1. Clone repository:
   ```bash
   git clone https://github.com/your-repo/ethiopian-medical-data-platform.git
   cd ethiopian-medical-data-platform
Configure environment:

bash
cp .env.example .env
# Edit with your Telegram API credentials
Start services:

bash
docker-compose up -d --build
Initialize database:

bash
docker-compose exec dbt python scripts/database/load_raw_data.py
🔍 Task Details
Task 1: Data Scraping
Key Components:

scripts/scraping/telegram_scraper.py: Main scraping script

scripts/scraping/image_downloader.py: Image download utility

Usage:

bash
docker-compose exec dbt python scripts/scraping/telegram_scraper.py
Output Structure:

text
data/raw/
├── telegram_messages/
│   └── YYYY-MM-DD/
│       └── channel_name.json
└── telegram_images/
    └── YYYY-MM-DD/
        └── channel_name/
            ├── 12345.jpg
            └── 12345.json
Task 2: Data Modeling
dbt Models:

Staging: stg_telegram_messages, stg_telegram_images

Dimensions: dim_channels, dim_dates

Facts: fct_messages, fct_image_detections

Run Transformations:

bash
docker-compose exec dbt bash
cd dbt/medical_analytics
dbt run
dbt test
Task 3: Object Detection
Processing Script:

bash
docker-compose exec dbt python app/object_detection/process_images.py
Detection Schema:

sql
CREATE TABLE analytics.fct_image_detections (
    detection_key VARCHAR(255) PRIMARY KEY,
    message_id INTEGER REFERENCES fct_messages,
    class_name VARCHAR(50),
    confidence FLOAT,
    is_medical BOOLEAN
);
Task 4: Analytical API
Endpoints:

GET /api/analytics/top-products

GET /api/channels/{channel}/activity

GET /api/search/messages?query=

Access API:

bash
curl http://localhost:8000/api/analytics/top-products?limit=5
Task 5: Orchestration
Run Pipeline:

bash
dagster dev -f orchestration/__init__.py
Scheduled Jobs:

python
# Runs daily at 2 AM
daily_pipeline_schedule = ScheduleDefinition(
    job=medical_data_pipeline,
    cron_schedule="0 2 * * *"
)
📚 API Documentation
Endpoint	Method	Parameters	Description
/api/analytics/top-products	GET	limit: int	Top mentioned products
/api/channels/activity	GET	period: enum(day,week,month)	Posting frequency trends
/api/search/messages	GET	query: str, channel: str	Full-text message search
💡 Usage Examples
Sample API Request:

bash
curl "http://localhost:8000/api/analytics/top-products?limit=3"
Expected Response:

json
[
  {
    "product_name": "paracetamol",
    "mention_count": 142,
    "channels": ["chemed", "tikvahpharma"]
  },
  {
    "product_name": "amoxicillin",
    "mention_count": 98,
    "channels": ["chemed"]
  }
]
Sample SQL Query:

sql
-- Find channels with most visual content
SELECT 
    c.channel_name,
    COUNT(d.detection_key) AS medical_images
FROM analytics.dim_channels c
JOIN analytics.fct_messages m ON c.channel_key = m.channel_key
JOIN analytics.fct_image_detections d ON m.message_key = d.message_key
WHERE d.is_medical = TRUE
GROUP BY 1
ORDER BY 2 DESC;
🤝 Contributing
Fork the repository

Create feature branch (git checkout -b feature/improvement)

Commit changes (git commit -m 'Add new feature')

Push to branch (git push origin feature/improvement)

Open a Pull Request

📜 License
MIT License - See LICENSE for details.

text

Key features of this README:
1. **Task-Oriented Structure**: Clear separation of all 5 tasks with implementation details
2. **Visual Hierarchy**: Consistent section headers with emojis
3. **Executable Code**: Ready-to-run commands for each component
4. **API Documentation**: Structured endpoint reference
5. **Data Flow**: Shows how components connect
6. **Project Navigation**: Quick links to key sections

The document balances technical depth with usability, providing both high-level overview and specific implementation details. Would you like me to add any additional sections or modify the existing ones?