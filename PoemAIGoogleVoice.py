import openai
import os
import time
from google.cloud import texttospeech

# Set API keys and environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Use an environment variable for security
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "poem-0-matic-b9f292c4f549.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def speak_text_google(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        name="en-US-Wavenet-F"
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    os.system("afplay output.mp3")  # for MacOS
    os.remove("output.mp3")  # Deletes the output.mp3 file after playing it

def get_user_choice(options, prompt):
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        try:
            choice = int(input("\nEnter your choice (number): "))
            if 1 <= choice <= len(options):
                return options[choice-1]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def generate_poem_with_openai():
    # Choices
    colors = ["Red", "Yellow", "Blue", "Orange", "Green"]
    locations = ["Miami Beach", "Downtown Miami", "Wynwood Miami", "Underline Miami", "Little Havana, Miami"]
    feelings = ["Happy", "Anxious", "Nostalgic", "Frustrated", "Romantic"]
    wildcards = ["Mojito", "Music", "Magic", "Epic", "Books"]
    poem_styles = ["Sonnet", "Haiku", "Free Verse", "Limerick", "Villanelle"]

    while True:
        color_choice = get_user_choice(colors, "Choose a color:")
        location_choice = get_user_choice(locations, "Choose a location:")
        feeling_choice = get_user_choice(feelings, "Choose a feeling:")
        wildcard_choice = get_user_choice(wildcards, "Choose a wildcard:")
        poem_style_choice = get_user_choice(poem_styles, "Choose a poem style:")

        clear_screen()
        choices = {
            "Color": color_choice,
            "Location": location_choice,
            "Feeling": feeling_choice,
            "Wildcard": wildcard_choice,
            "Poem Style": poem_style_choice
        }
        for key, value in choices.items():
            print(f"{key}: {value}")
            speak_text_google(f"{key}: {value}")
        proceed = input("\nDo you want to proceed with these choices? (yes/no): ").strip().lower()
        if proceed == 'yes':
            break
        elif proceed == 'no':
            print("\nOkay, let's reselect your choices!")
            continue
        else:
            print("\nInvalid input. Please answer with 'yes' or 'no'.")
            continue

    prompt = (f"Write a {poem_style_choice} about {location_choice} with themes of {color_choice}, "
             f"{feeling_choice}, and {wildcard_choice}.")

    retries = 3
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": prompt}])
            content = response.get('choices', [{}])[0].get('message', {}).get('content')
            if content:
                return content.strip()
            else:
                return "Error: The response from OpenAI was unexpected."
        except openai.error.OpenAIError as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            else:
                return f"OpenAI Error after {retries} attempts: {e}"
        except Exception as e:
            return f"Error generating poem: {e}"

clear_screen()
print("Poem-O-Matic-AI by MarioTheMaker\n")
poem = generate_poem_with_openai()
print(poem + "\n")
speak_text_google(poem)
time.sleep(2)
sign_off = "Poem Created by Poem-O-Matic-AI by Mario Cruz for O'Miami festival"
print(sign_off)
speak_text_google(sign_off)
