import prefect
from prefect import task
import tensorflow as tf

@task
def evaluate_model(model_path: str, data: dict) -> dict:
    """Evaluates the trained image classification model."""
    logger = prefect.get_run_logger()
    logger.info("Evaluating image classification model...")
    
    test_ds = data["test_ds"] 
    
    try:
        model = tf.keras.models.load_model(model_path)
        
        # Evaluate using the test dataset
        loss, accuracy = model.evaluate(test_ds, verbose=0)
        
        metrics = {"loss": loss, "accuracy": accuracy}
        logger.info(f"Model evaluation complete. Metrics: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error during model evaluation: {e}")
        raise