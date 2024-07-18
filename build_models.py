
#import libraries 

from roboflow import Roboflow
import supervision as sv
import cv2
import io 

import matplotlib.pyplot as plt
from PIL import Image 
import os
import re
from dotenv import load_dotenv

#Load API_KEYS
load_dotenv()
ROBO_API_KEY= os.getenv("ROBO_API_KEY")

# Initialize the box annotator and API
box_annotator = sv.BoxAnnotator()

from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key= ROBO_API_KEY
)



def process_image(file_path):
    result = CLIENT.infer(file_path, model_id="openvission/2")
    detections = sv.Detections.from_inference(result)

    # filter by class
    detections = detections[detections.class_id == 0]
    #print(len(detections))


    labels = [item["class"] for item in result["predictions"]]
    # Initialize the box annotator
    box_annotator = sv.BoxAnnotator()

    detections = sv.Detections.from_roboflow(result)

    label_annotator = sv.LabelAnnotator()

    image = cv2.imread(file_path)

    annotated_image = box_annotator.annotate(
        scene=image, detections=detections)
    annotated_image = label_annotator.annotate(
        scene=annotated_image, detections=detections, labels=labels)

    # Plot the annotated image using matplotlib and save it
    plt.figure(figsize=(16, 16))
    plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for correct color display
    plt.axis('off')  # Hide the axis
   
    # Getting the current figure and save it in the variable. 
    fig = plt.gcf() 
    plt.close()  # Close the plot to avoid displaying it
    return [fig,labels]
   


# convert to image
def fig2img(fig): 
    buf = io.BytesIO() 
    fig.savefig(buf) 
    buf.seek(0) 
    img = Image.open(buf) 
    return img 

# List of strings with currency
# Count the number of coins 
def count_coins(lst):
    # Extract numbers and sum them
    total_sum = sum(int(re.search(r'\d+', item).group()) for item in lst)

    results= {"Number of coin": len(lst),
              "Total amount ": total_sum}
    return results