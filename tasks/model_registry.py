import prefect
from prefect import task

@task
def register_model(model_path: str, metrics: dict, version: str = "1.0"):
    """Simulates registering the model and its metrics."""
    logger = prefect.get_run_logger()
    logger.info(f"Registering model version {version} with metrics: {metrics}")
    # In a real scenario, you'd interact with an ML Registry (e.g., MLflow, ClearML) to store model artifacts, metrics, and metadata.
    logger.info(f"Model {model_path} registered successfully.")