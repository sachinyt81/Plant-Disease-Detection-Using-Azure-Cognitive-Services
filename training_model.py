"""Importing Libraries"""
import os
import time
import uuid
import sys
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, \
    ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials

# Replace with valid values
ENDPOINT = "https://frtproject.cognitiveservices.azure.com/"
TRAINING_KEY = "cd0c424426ec4f6ebbc58badbc49c06a"
PREDICTION_KEY = "cd0c424426ec4f6ebbc58badbc49c06a"
PREDICTION_RESOURCE_ID = "/subscriptions/b9e78343-1e6b-48e3-b4a2-af03b3a0cb20/" \
                         "resourceGroups/cloud-shell-storage-centralindia/providers/Microsoft.CognitiveServices" \
                         "/accounts/frtproject"
CREDENTIALS = ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY})
TRAINER = CustomVisionTrainingClient(ENDPOINT, CREDENTIALS)
PREDICTION_CREDENTIALS = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
PREDICTOR = CustomVisionPredictionClient(ENDPOINT, PREDICTION_CREDENTIALS)
PUBLISH_ITERATION_NAME = "classifyModel"

CREDENTIALS = ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY})
TRAINER = CustomVisionTrainingClient(ENDPOINT, CREDENTIALS)

# Create a new project
print("Creating project...")
project_name = uuid.uuid4()
project = TRAINER.create_project(project_name)

# Make tags as per necessity in the new project
pbs_tag = TRAINER.create_tag(project.id, "Pepper_bell_Bacterial_spot")
pbh_tag = TRAINER.create_tag(project.id, "Pepper_bell_Healthy")
peb_tag = TRAINER.create_tag(project.id, "Potato_EarlyBlight")
ph_tag = TRAINER.create_tag(project.id, "Potato_Healthy")
teb_tag = TRAINER.create_tag(project.id, "Tomato_Early_Blight")
th_tag = TRAINER.create_tag(project.id, "tomato_Healthy")
base_image_location = os.path.join(os.path.dirname(__file__), "Images")
print("Adding images...")

image_list = []

# Uploading images to Azure Cognitive Services
for image_num in range(1, 11):
    file_name = "PBBS{}.jfif".format(image_num)
    with open(os.path.join(base_image_location, "Pepper_bell_Bacterial_spot", file_name), "rb") \
            as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(),
                                               tag_ids=[pbs_tag.id]))

for image_num in range(1, 11):
    file_name = "PH{}.jfif".format(image_num)
    with open(os.path.join(base_image_location, "Pepper_bell_Healthy", file_name), "rb") \
            as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(),
                                               tag_ids=[pbh_tag.id]))

for image_num in range(1, 11):
    file_name = "PEB{}.jfif".format(image_num)
    with open(os.path.join(base_image_location, "Potato_EarlyBlight", file_name), "rb") \
            as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(),
                                               tag_ids=[peb_tag.id]))

for image_num in range(1, 11):
    file_name = "PH{}.jfif".format(image_num)
    with open(os.path.join(base_image_location, "Potato_Healthy", file_name), "rb") \
            as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(),
                                               tag_ids=[ph_tag.id]))

for image_num in range(1, 11):
    file_name = "TEB{}.jfif".format(image_num)
    with open(os.path.join(base_image_location, "Tomato_Early_Blight", file_name), "rb") \
            as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(),
                                               tag_ids=[teb_tag.id]))

for image_num in range(1, 11):
    file_name = "TH{}.jfif".format(image_num)
    with open(os.path.join(base_image_location, "Tomato_Healthy", file_name), "rb") \
            as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(),
                                               tag_ids=[th_tag.id]))

upload_result = TRAINER.create_images_from_files(project.id,
                                                 ImageFileCreateBatch(images=image_list))
if not upload_result.is_batch_successful:
    print("Image batch upload failed.")
    for image in upload_result.images:
        print("Image status: ", image.status)
    sys.exit()
print("Training...")
iteration = TRAINER.train_project(project.id)
while iteration.status != "Completed":
    iteration = TRAINER.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    print("Waiting 10 seconds...")
    time.sleep(10)
# The iteration is now trained. Publish it to the project endpoint
TRAINER.publish_iteration(project.id, iteration.id, PUBLISH_ITERATION_NAME, PREDICTION_RESOURCE_ID)
print("Done!")

# Now there is a trained endpoint that can be used to make a prediction
PREDICTION_CREDENTIALS = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
PREDICTOR = CustomVisionPredictionClient(ENDPOINT, PREDICTION_CREDENTIALS)
result_tag = {}
with open(os.path.join(base_image_location, "Test/test_image.jfif"), "rb") as image_contents:
    results = PREDICTOR.classify_image(
        project.id, PUBLISH_ITERATION_NAME, image_contents.read())

    # Display the results.2
    for prediction in results.predictions:
        result_tag[prediction.tag_name] = prediction.probability * 100

    result = max(result_tag, key=lambda x: result_tag[x])
    # Remedies for plants diseases
    if result == "Tomato_Early_Blight":
        print("Symptoms: Tomato Early Blight\n"
              "Diseases: Alternaria Solani\n"
              "Remedy: Bacillus Subtilis, Hydroperoxyl\n")
    elif result == "Pepper_bell_Bacterial_spot":
        print("Symptoms: Bell Pepper Blight\n"
              "Diseases: Stem phylium solani\n"
              "Remedy: Liquid copper\n")
    elif result == "Potato_EarlyBlight":
        print("Symptoms: Potato Early Blight\n"
              "Diseases: Colletotrichum coccodes\n"
              "Remdy:	Azoxystrobin\n")
    else:
        print("Plant is Healthy\n")
