import os
from urllib.request import urlopen, Request
import base64
from pathlib import Path
from dotenv import load_dotenv

# Add references
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
            azure_endpoint=azure_endpoint,
            api_version=api_version_name
        )
                

        # Initialize prompts
        system_message = "You are an AI assistant in a grocery store that sells fruit. You provide detailed answers to questions about produce."
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the image\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")


                # Get a response to image input
                image_url = "images/orange.jpeg"
                image_format = "jpeg"
                with open(image_url, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("utf-8")

                data_url = f"data:image/{image_format};base64,{image_data}"


                response = client.chat.completions.create(
                    model=deployment_name,
                    messages=[
                        {"role": "system", "content": system_message},
                        { "role": "user", "content": [  
                            { "type": "text", "text": prompt},
                            { "type": "image_url", "image_url": {"url": data_url}}
                        ] } 
                    ]
                )
                print(response.choices[0].message.content)    


    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()