import os
import requests
import base64
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment_name = os.getenv("MODEL_DEPLOYMENT")
        api_version_name = os.getenv("API_VERSION_NAME")

        # Initialize the project client
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2025-01-01-preview",  # important for multimodal
            azure_endpoint=azure_endpoint
        )


        # Initialize prompts
        system_message = "You are an AI assistant for a produce supplier company."
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the audio\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")

                # Encode the audio file
                file_path = "data/avocados.mp3"
                with open(file_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    audio_data = base64.b64encode(audio_bytes).decode("utf-8")

                # Get a response to audio input
                # Get a response to audio input
                response = client.chat.completions.create(
                    model=deployment_name,
                    messages=[
                        {"role": "system", "content": system_message},
                        { "role": "user",
                            "content": [
                            { 
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "input_audio",
                                "input_audio": {
                                    "data": audio_data,
                                    "format": "mp3"
                                }
                            }
                        ] }
                    ]
                )
                print(response.choices[0].message.content)


    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()