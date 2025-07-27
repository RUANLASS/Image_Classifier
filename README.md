# Image_Classifier
A basic image classification pipeline using Prefect 2.x. 

An end-to-end Machine Learning pipeline for image classification, orchestrated using Prefect 2.x. This project demonstrates a full ML workflow, from data ingestion and preprocessing to model training, evaluation, and registration. 
Pipeline Stages:
Data Ingestion: Downloads or loads image datasets.
Data Preprocessing: Cleans, augments, and prepares image data for model training.
Model Training: Trains an image classification model (e.g., using TensorFlow/Keras).
Model Evaluation: Assesses the trained model's performance on a test set.
Model Registration/Logging: (Placeholder for future enhancement or simple logging, as discussed).
Technologies Used
Python 3.11.9
Prefect 2.14.20: Workflow orchestration, task/flow definition, deployments, server, worker.
TensorFlow / Keras: (Assuming these were used for the ML model) For building and training the image classification model.
SQLite: Prefect's default local database for metadata.
Setup & Installation
Follow these steps to set up and run the project locally.
1. Clone the Repository
Bash
git clone https://github.com/[Your GitHub Username]/[Your Project Repository Name].git
cd [Your Project Repository Name] # e.g., ML_2_Ref_SplitDataset

2. Python Environment Setup
We will set up a specific Python version and a virtual environment for isolated dependencies.
Bash
pyenv install 3.11.9

pyenv local 3.11.9

python --version

python -m venv venv
source venv/bin/activate

3. Install Dependencies
Install all necessary Python packages, including Prefect 2.x, from requirements.txt.
Bash
pip install -r requirements.txt
4. Configure Prefect API URL
Set the environment variable for your local Prefect Server. This needs to be done in every new terminal session where you interact with Prefect.
Bash
export PREFECT_API_URL="http://127.0.0.1:4200/api"

5. Start Prefect Server (Terminal 1)
Open a new terminal window for this step.
Bash
cd #to your directory
source venv/bin/activate 
export PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect server start

6. Start Prefect Worker (Terminal 2)
Open a second new terminal window.
Bash
cd 
source venv/bin/activate 
export PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect worker start -q 'default'

7. Create Prefect Work Pool (If not already created)
Open a third new terminal window.
Bash

venv/bin/prefect work-pool create pool

You should see: Work pool 'pool' created successfully!
Usage: Register and Run the Pipeline
1. Register the Deployment (Terminal 3)
In the same third terminal window (or a new one), run your pipeline script. This will execute the flow locally and register its deployment with the Prefect server.
Bash
python pipeline.py 
2. Access the Prefect UI
Open your web browser and go to: http://localhost:4200
Navigate to the "Deployments" section to see your registered pipeline.
Go to the "Flow Runs" section to see current and historical runs.
3. Trigger a Deployment Run (from UI or CLI)
Now that your deployment is registered, you can trigger new runs via the UI or CLI without rerunning python pipeline.py. The Prefect Worker (Terminal 2) will pick these up.
From UI: Go to Deployments -> select your deployment -> Click "Run".
From CLI (New Terminal):
Bash
cd ____
source venv/bin/activate
export PREFECT_API_URL="http://127.0.0.1:4200/api"
Future Enhancements
Model Registry Integration: Integrate with tools like MLflow or Weights & Biases for more comprehensive model versioning and tracking.
Advanced Error Handling: Implement custom retry strategies and failure notifications.
Cloud Deployment: Extend the setup to deploy the Prefect Server and Worker on cloud platforms (e.g., AWS, GCP, Azure) for scalable execution.
Data Versioning: Incorporate DVC (Data Version Control) to manage dataset versions.
Pre-commit Hooks/CI/CD: Add automated checks and deployment pipelines for code quality and continuous integration.

