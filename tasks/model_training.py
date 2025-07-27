import prefect
from prefect import task
import os
import tensorflow as tf
from tensorflow.keras import layers, models

@task
def train_model(data: dict, epochs: int = 5) -> str:
    logger = prefect.get_run_logger()
    logger.info("Training image classification model...")

    train_ds = data["train_ds"]
    val_ds = data["val_ds"]
    num_classes = data["num_classes"]
    img_height, img_width = data["img_size"]

    #Simple Neural Network
    model = models.Sequential([
        # Data augmentation 
        layers.RandomFlip("horizontal", input_shape=(img_height, img_width, 3)),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),

        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax') # Use softmax for multi-class classification
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])
    
    model.summary(print_fn=lambda x: logger.info(x)) 

    # Train the model 
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )
    
    #Saving the model
    model_path = "models/my_image_classifier_model.h5"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)
    logger.info(f"Model trained and saved to {model_path}")

    # Logging accuracy
    final_accuracy = history.history['accuracy'][-1]
    final_val_accuracy = history.history['val_accuracy'][-1]
    logger.info(f"Final Training Accuracy: {final_accuracy:.4f}")
    logger.info(f"Final Validation Accuracy: {final_val_accuracy:.4f}")

    return model_path