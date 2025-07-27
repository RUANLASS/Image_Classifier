import prefect
from prefect import task
import os
import shutil # For cleaning up dummy data if generated
import numpy as np
from PIL import Image

@task
def ingest_data(
    data_dir: str = "data/",
    num_dummy_images_per_class: int = 20,
    num_classes: int = 2,
    img_size: tuple = (64, 64)
) -> dict:
   
    logger = prefect.get_run_logger()
    train_dir = os.path.join(data_dir, "train")
    test_dir = os.path.join(data_dir, "test") 

    # Checking if any actual data exists
    has_real_data = False
    if os.path.exists(train_dir) and any(os.listdir(train_dir)):
        has_real_data = True
        logger.info(f"Real data found in '{train_dir}'. Skipping dummy data generation.")
        # Check for test data
        if os.path.exists(test_dir) and any(os.listdir(test_dir)):
            logger.info(f"Real test data found in '{test_dir}'.")
            return {"train_dir": train_dir, "test_dir": test_dir}
        else:
            logger.warning(f"No real test data found in '{test_dir}'. Train/Validation split will be used for testing.")
            return {"train_dir": train_dir, "test_dir": None} 

    # Generating dummy data 
    if not has_real_data:
        logger.warning(f"No real data found in '{train_dir}'. Generating dummy data for demonstration.")
        if os.path.exists(train_dir):
            shutil.rmtree(train_dir)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True) # Create test dir for dummy data

        for class_idx in range(num_classes):
            class_name = f"class_{class_idx}"
            train_class_path = os.path.join(train_dir, class_name)
            test_class_path = os.path.join(test_dir, class_name)
            os.makedirs(train_class_path, exist_ok=True)
            os.makedirs(test_class_path, exist_ok=True)

            for i in range(num_dummy_images_per_class):
                # Create dummy image
                dummy_image_data = np.random.randint(0, 256, size=(img_size[0], img_size[1], 3), dtype=np.uint8)
                img = Image.fromarray(dummy_image_data)

                # Save to train
                img.save(os.path.join(train_class_path, f"img_{i}.png"))
                # Save some to test (e.g., first 20% go to test)
                if i < num_dummy_images_per_class * 0.2:
                     img.save(os.path.join(test_class_path, f"img_test_{i}.png"))

        logger.info(f"Generated {num_dummy_images_per_class * num_classes} dummy images per split in '{data_dir}'.")
        return {"train_dir": train_dir, "test_dir": test_dir}