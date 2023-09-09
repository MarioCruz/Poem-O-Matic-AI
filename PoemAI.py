import openai
import os

# Ensure you have your API key set up
openai.api_key = os.environ.get('OPENAI_API_KEY')  # Use an environment variable for security

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_choice(options, prompt):
    """Get user's choice from the provided options."""
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
    """Generate a poem based on user's choices using OpenAI."""
    colors = ["Red", "yellow", "Blue", "orange", "green"]
    locations = ["Miami Beach", "Downtown Miami", "Wynwood Miami", "underline Miami", "Little Havana, Miami"]
    feelings = ["Happy", "Anxious", "nostalgic", "frustrated", "romantic"]
    wildcards = ["Mojito", "music", "magic", "epic", "books"]
    poem_styles = ["Sonnet", "Haiku", "Free Verse", "Limerick", "Villanelle"]

    color_choice = get_user_choice(colors, "Choose a color:")
    location_choice = get_user_choice(locations, "Choose a location:")
    feeling_choice = get_user_choice(feelings, "Choose a feeling:")
    wildcard_choice = get_user_choice(wildcards, "Choose a wildcard:")
    poem_style_choice = get_user_choice(poem_styles, "Choose a poem style:")

    # Create the prompt
    prompt = (f"Write a {poem_style_choice} about {location_choice} with themes of {color_choice}, "
             f"{feeling_choice}, and {wildcard_choice}.")

    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": prompt}])

        # Check if the response has the expected structure
        if 'choices' in response and len(response['choices']) > 0 \
           and 'message' in response['choices'][0] \
           and 'content' in response['choices'][0]['message']:
            return response['choices'][0]['message']['content'].strip()
        else:
            # Return a default message if the response structure is unexpected
            return "Error: The response from OpenAI was unexpected."

    except Exception as e:
        # Catch any other errors from the API call
        return f"Error generating poem: {e}"

# Clear the screen
clear_screen()

# Display the Poem
print("Poem-O-Matic-AI by MarioTheMaker\n")
poem = generate_poem_with_openai()
print(poem + "\n")
