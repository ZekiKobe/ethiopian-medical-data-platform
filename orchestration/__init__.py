
# orchestration/__init__.py
"""
Dagster pipeline definitions for Ethiopian Medical Data Platform
"""

# Explicitly expose definitions for Dagster discovery
from .definitions import defs as __all__  # noqa: F401
from orchestration.definitions import defs
# Import all assets to ensure they're registered
from .assets import (
    scrape_telegram_data,
    load_raw_data,
    run_dbt_transformations,
    process_images_with_yolo,
    generate_api_specs
)

# Import jobs and schedules
from .jobs import medical_data_pipeline
from .schedules import daily_pipeline_schedule

# Optional: Expose selected objects for direct import
__all__ = [
    'scrape_telegram_data',
    'load_raw_data',
    'run_dbt_transformations',
    'process_images_with_yolo',
    'generate_api_specs',
    'medical_data_pipeline',
    'daily_pipeline_schedule'
]