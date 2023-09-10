import requests
import cv2
import os
import openai
import time

# Azure setup
API_KEY = os.getenv('AZURE_API_KEY')
ENDPOINT = 'https://?E-to-text.cognitiveservices.azure.com/'
DESCRIBE_URL = f'{ENDPOINT}/vision/v3.1/describe'
ANALYZE_URL = f'{ENDPOINT}/vision/v3.1/analyze'

headers = {
    'Ocp-Apim-Subscription-Key': API_KEY,
    'Content-Type': 'application/octet-stream'
}

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def capture_image():
    cam = cv2.VideoCapture(0)
    time.sleep(2)
    ret, frame = cam.read()
    cam.release()
    return ret, frame

def send_image_to_azure(url, image):
    _, img_encoded = cv2.imencode('.jpg', image)
    response = requests.post(url, headers=headers, data=img_encoded.tobytes())
    return response.json()

def create_poem(description):
    prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Write a poem inspired by the image description: {description}"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    success, captured_img = capture_image()
    if not success:
        print("Failed to grab frame from camera. Check camera availability.")
        exit()

    # Get description
    response_data = send_image_to_azure(DESCRIBE_URL, captured_img)
    primary_description = ""
    if 'description' in response_data and response_data['description']['captions']:
        primary_description = response_data['description']['captions'][0]['text']

    if primary_description:
        print("Image Description:", primary_description)

        poem = create_poem(primary_description)
        print("\nGenerated Poem:\n", poem)

        # Get color analysis
        response_data = send_image_to_azure(ANALYZE_URL, captured_img)
        if 'color' in response_data:
            dominant_color_foreground = response_data['color']['dominantColorForeground']
            dominant_colors = response_data['color']['dominantColors']
            print(f"\nDominant Foreground Color: {dominant_color_foreground}")
            print("Dominant Colors:", ", ".join(dominant_colors))
    else:
        print("Couldn't retrieve a description for the image.")
