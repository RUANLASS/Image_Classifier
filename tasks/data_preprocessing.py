import prefect
from prefect import task
import tensorflow as tf
import os

@task
def preprocess_data(
    data_dirs: dict,
    img_size: tuple = (128, 128),
    batch_size: int = 32,
    validation_split: float = 0.2, # For splitting train_dir into train/validation. Final split= 3:1:1
    seed: int = 42
) -> dict:
    # Loads images, resizes, normalizes, creates tf.data.Dataset objects.
    logger = prefect.get_run_logger()
    logger.info("Preprocessing image data using TensorFlow's utilities...")

    train_dir = data_dirs.get("train_dir")
    test_dir = data_dirs.get("test_dir")

    if not train_dir or not os.path.exists(train_dir):
        raise ValueError("Training data directory not provided or does not exist.")

    train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
        directory=train_dir,
        labels='inferred',
        label_mode='int', 
        image_size=img_size,
        interpolation='nearest',
        batch_size=batch_size,
        shuffle=True, 
        seed=seed,
        validation_split=validation_split,
        subset='both' 
    )
    
    # Log class names
    class_names = train_ds.class_names
    num_classes = len(class_names)
    logger.info(f"Found {num_classes} classes: {class_names}")

   
    test_ds = None
    if test_dir and os.path.exists(test_dir) and any(os.listdir(test_dir)):
        test_ds = tf.keras.utils.image_dataset_from_directory(
            directory=test_dir,
            labels='inferred',
            label_mode='int',
            image_size=img_size,
            interpolation='nearest',
            batch_size=batch_size,
            shuffle=False, 
            seed=seed 
        )
        logger.info(f"Loaded {len(test_ds) * batch_size} samples for separate test set.")
    else:
        logger.warning("No separate test directory found. The 'validation' split will serve as the test set for evaluation.")
        test_ds = val_ds # If no dedicated test set, use validation for evaluation

    # Normalize pixel values to [0, 1]
    normalization_layer = tf.keras.layers.Rescaling(1./255)

    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y)).cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y)).cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y)).cache().prefetch(buffer_size=tf.data.AUTOTUNE) # Apply to test as well

    logger.info("Image preprocessing complete. Datasets ready for training.")
    
    return {
        "train_ds": train_ds,
        "val_ds": val_ds, 
        "test_ds": test_ds, 
        "num_classes": num_classes,
        "class_names": class_names,
        "img_size": img_size
    }