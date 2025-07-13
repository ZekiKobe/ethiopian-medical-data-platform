# Ethiopian Medical Data Platform

![Data Pipeline Architecture](docs/pipeline_architecture.png) *(placeholder for architecture diagram)*

An end-to-end data platform that extracts medical business insights from public Telegram channels in Ethiopia, processes the data through a modern ELT pipeline, and exposes analytical insights via API.

## 🚀 Features

- **Telegram Data Scraping**: Collect messages and images from public medical channels
- **Data Lake Storage**: Store raw data in a structured, partitioned format
- **PostgreSQL Data Warehouse**: Reliable storage with optimized schema
- **dbt Transformations**: Clean, model, and document data using best practices
- **YOLO Object Detection**: Enrich image data with detected medical products
- **FastAPI Analytics**: RESTful endpoints for business insights
- **Dagster Orchestration**: Reliable pipeline scheduling and monitoring

## 📊 Business Questions Answered

1. Top 10 most mentioned medical products/drugs across channels
2. Price/availability variations of specific products
3. Channels with most visual content (pills vs. creams)
4. Daily/weekly trends in health-related posting volume

## 🛠️ Technical Stack

| Component          | Technology               |
|--------------------|--------------------------|
| Data Extraction    | Telethon (Telegram API)  |
| Data Storage       | PostgreSQL               |
| Data Transformation| dbt (Data Build Tool)    |
| Data Modeling      | Star Schema              |
| Image Processing   | YOLOv8 (Ultralytics)     |
| API Layer          | FastAPI                  |
| Orchestration      | Dagster                  |
| Infrastructure     | Docker, Docker Compose   |

## 🏗️ Project Structure


## 🏁 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Telegram API credentials

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ethiopian-medical-data-platform.git
   cd ethiopian-medical-data-platform

## Set up environment:
cp .env.example .env
# Edit .env with your credentials
## Build and start services:
docker-compose up -d --build

## Initialize dbt:
docker-compose exec dbt bash
cd dbt/medical_analytics
dbt deps
dbt run

Running the Pipeline
Scrape Telegram data:

bash
docker-compose exec dbt python scripts/scraping/telegram_scraper.py
Process images with YOLO:

bash
docker-compose exec dbt python app/object_detection/process_images.py
Access the API:

Swagger docs: http://localhost:8000/docs

Example endpoint: GET /api/v1/top_products?limit=10

📈 Example Queries
sql
-- Top 10 mentioned products
SELECT 
    UNNEST(product_mentions) AS product,
    COUNT(*) AS mentions
FROM analytics.fct_messages
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;
🤝 Contributing
Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📜 License
Distributed under the MIT License. See LICENSE for more information.

📧 Contact
Project Maintainer - [Your Name] - your.email@example.com

Project Link: https://github.com/your-repo/ethiopian-medical-data-platform

text

## Key Improvements Included:

1. **Visual Hierarchy**: Clear section headers with emojis for better scanning
2. **Business Value**: Front-loaded the key business questions answered
3. **Technical Depth**: Detailed stack table and architecture overview
4. **Getting Started**: Concise setup instructions with docker commands
5. **Usage Examples**: Sample SQL query showing analytical value
6. **Project Structure**: Visual tree showing critical directories
7. **Maintenance Info**: Contribution guidelines and license

Would you like me to add any specific sections like:
- API endpoint documentation
- Data dictionary
- Troubleshooting guide
- Performance benchmarks
- Roadmap of future features?