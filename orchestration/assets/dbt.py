from dagster import asset, Output
import subprocess

@asset(deps=["load_raw_data"])
def run_dbt_transformations():
    """Run dbt transformations"""
    result = subprocess.run(
        ["dbt", "run"],
        cwd="dbt/medical_analytics",
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    
    return Output(
        None,
        metadata={
            "success": True,
            "logs": result.stdout
        }
    )