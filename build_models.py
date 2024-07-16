
#import libraries 

from roboflow import Roboflow
import supervision as sv
import cv2

import matplotlib.pyplot as plt
from PIL import Image 
import io 

# Initialize the box annotator and API
box_annotator = sv.BoxAnnotator()

from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="wrNmIilZnQ3q9s6VsVxd"
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
   

#process_image(file_path)

# sv.plot_image()

# def fig2img(fig): 
#     buf = io.BytesIO() 
#     fig.savefig(buf) 
#     buf.seek(0) 
#     img = Image.open(buf) 
#     return img 
  