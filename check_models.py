from openai import OpenAI

# Make sure you have set your OpenAI API key
client = OpenAI()

def list_available_models():
    try:
        # Fetch the list of models
       models = client.models.list()
       for model in models.data:
            print(model.id)

        
    except Exception as e:
        print(f"Error fetching models: {e}")

# Call the function
list_available_models()
