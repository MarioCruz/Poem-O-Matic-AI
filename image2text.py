import requests
import cv2
import json
import time

# Azure setup
API_KEY = 'xxxxxxxx'  # Remember to secure this better
ENDPOINT = 'AzureEndpoint'
DESCRIBE_URL = f'{ENDPOINT}/vision/v3.1/describe'
ANALYZE_URL = f'{ENDPOINT}/vision/v3.1/analyze'

# Capture image using OpenCV
cam = cv2.VideoCapture(0)
time.sleep(2)  # waits for 2 seconds
ret, frame = cam.read()
cam.release()

if not ret:
    print("Failed to grab frame from camera. Check camera availability.")
    exit()

img_path = "captured_image.jpg"
cv2.imwrite(img_path, frame)

headers = {
    'Ocp-Apim-Subscription-Key': API_KEY,
    'Content-Type': 'application/octet-stream'
}

# Get descriptions
params_describe = {
    'maxCandidates': '5',
    'language': 'en'
}

with open(img_path, 'rb') as f:
    response = requests.post(DESCRIBE_URL, headers=headers, params=params_describe, data=f.read())

response_data = response.json()

# Extract and print description from the response
if 'description' in response_data:
    captions = response_data['description']['captions']
    for caption in captions:
        print(caption['text'], "- Confidence:", caption['confidence'])
else:
    print(json.dumps(response_data, indent=4))

# Get color information
params_analyze = {
    'visualFeatures': 'Color',
    'language': 'en'
}

with open(img_path, 'rb') as f:
    response = requests.post(ANALYZE_URL, headers=headers, params=params_analyze, data=f.read())

response_data = response.json()

# Extract and print color information from the response
if 'color' in response_data:
    dominant_color_foreground = response_data['color']['dominantColorForeground']
    dominant_colors = response_data['color']['dominantColors']

    print(f"\nDominant Foreground Color: {dominant_color_foreground}")
    print("Dominant Colors:", ", ".join(dominant_colors))
else:
    print(json.dumps(response_data, indent=4))
