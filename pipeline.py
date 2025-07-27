import prefect
from prefect import flow
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import IntervalSchedule
import datetime

from tasks.data_ingestion import ingest_data
from tasks.data_preprocessing import preprocess_data
from tasks.model_training import train_model
from tasks.model_evaluation import evaluate_model
from tasks.model_registry import register_model

#FLOW:
@flow(name="Image Classification Pipeline from Uploaded Data")
def image_classification_pipeline(
    data_directory: str = "data/", 
    epochs: int = 5,
    img_height: int = 128,
    img_width: int = 128,
    batch_size: int = 32
):
    logger = prefect.get_run_logger()
    logger.info("Starting image classification pipeline from uploaded data...")

    # return: train/test directories path
    data_paths = ingest_data(
        data_dir=data_directory,
        num_dummy_images_per_class=50, 
        num_classes=2, 
        img_size=(img_height, img_width)
    )

    # return: tf.data.Dataset objects
    processed_datasets = preprocess_data(
        data_dirs=data_paths,
        img_size=(img_height, img_width),
        batch_size=batch_size
    )

    # input: tf.data.Dataset object of train dataset, return: model .h5 file 
    model_path = train_model(data=processed_datasets, epochs=epochs)

    # input: tf.data.Dataset of test dataset, return: {loss, accuracy}
    metrics = evaluate_model(model_path=model_path, data=processed_datasets)

    
    register_model(model_path=model_path, metrics=metrics, version="1.0")

    logger.info("Image classification pipeline from uploaded data finished.")

# --- Run and Deploy the Flow ---

if __name__ == "__main__":

    print("--- Running flow locally ---")
    image_classification_pipeline(
        data_directory="data/",
        epochs=1, 
        img_height=64,
        img_width=64,
        batch_size=16
    )

    # 2. Create a Deployment (for scheduling/triggering in Prefect Cloud/Server), defining a schedule
    print("\n--- Creating Prefect Deployment ---")
    
    #Schedule
    next_sunday_1am = datetime.datetime(2025, 7, 27, 1, 0, 0) 
    today = datetime.date.today()
    days_until_sunday = (6 - today.weekday() + 7) % 7 
    if days_until_sunday == 0: 
        next_sunday = today
    else:
        next_sunday = today + datetime.timedelta(days=days_until_sunday)
    
    next_sunday_1am_dynamic = datetime.datetime(next_sunday.year, next_sunday.month, next_sunday.day, 1, 0, 0)

    weekly_schedule = IntervalSchedule(interval=datetime.timedelta(weeks=1), anchor_date=next_sunday_1am_dynamic)

    #Deployment
    deployment = Deployment.build_from_flow(
        flow=image_classification_pipeline,
        name="weekly-image-classifier-uploaded-data",
        version="1.0",
        schedule=weekly_schedule,
        parameters={
            "data_directory": "data/",
            "epochs": 10,
            "img_height": 128,
            "img_width": 128,
            "batch_size": 32
        },
        tags=["ml", "image-classification", "weekly", "uploaded-data"],
        work_queue_name="default",
        work_pool_name="pool"
    )
    deployment.apply()

    print("Deployment applied. Check Prefect UI to start the agent and run the flow.")