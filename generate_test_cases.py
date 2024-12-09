from openai import OpenAI
import os
import sys
import argparse
import json

client = OpenAI()


# Define function signatures
function_signatures = [
    {
        "name": "read_file",  # Ensure the function name is correctly defined here
        "description": "Read the content of the file at the specified path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to read."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    }
]

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            selected_lines = lines[0:5]
        return selected_lines
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except PermissionError:
        print(f"Error: You do not have permission to read the file {file_path}.")
    except Exception as e:
        print(f"Error: {e}")



# Function to read a file's contents
def read_file_content(file_path):
    tools = [{"type": "function", "function": function_signatures[0]}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are assisting with code analysis. Use the supplied tools to assist the user"},
            {"role": "user", "content": f"Read the file: {file_path}"}
        ],
        tools=tools
    )
    print("read file")
    print(response)
    tool_call = response.choices[0].message.tool_calls[0]
    print("tool call")
    print(tool_call)
    arguments = json.loads(tool_call.function.arguments)

    file_path = arguments.get('file_path')

    # Call the get_delivery_date function with the extracted order_id

    file_content = read_file(file_path)
    #print(file_content)
    function_call_result_message = {
    "role": "tool",
    "content": json.dumps({
        "file_path": file_path,
        "file_content":file_content
    }),
    "tool_call_id": response.choices[0].message.tool_calls[0].id
    }
    completion_payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a helpful with reading files. Use the supplied tools to assist the user."},
            {"role": "user", "content": "Hi, can you read file"},
            {"role": "assistant", "content": "Hi there! I can help with that. Can you please provide file_path"},
            {"role": "user", "content": f"File path {file_path}. Give me content of the file"},
            response.choices[0].message,
            function_call_result_message
        ]
    }

# Call the OpenAI API's chat completions endpoint to send the tool call result back to the model

    response = client.chat.completions.create(
        model=completion_payload["model"],
        messages=completion_payload["messages"]
    )

# Print the response from the API. In this case it will typically contain a message such as "The delivery date for your order #12345 is xyz. Is there anything else I can help you with?"
    print("file print")
    print(response)
    return response

# Function to generate unit tests
def generate_unit_tests(file_path,repo_name):
    tools = [{"type": "function_call", "functions": function_signatures[0]}]
    file_content=read_file(file_path)
    response=None
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are assisting with C/C++ code analysis. You will help in creating unit test cases to reproduce memory leaks if they exist in the code. The file content will be read using the provided tools."},
            {"role": "user", "content": f"I will give you the file content. Please generate unit test cases to reproduce any memory leaks that might exist in the file"},
            {"role": "assistant", "content": "Please share the code so I can read its contents and generate unit test cases to capture potential memory leaks."},
            {"role": "user", "content": f"Generate unit tests for memory leak issues in code\n {file_content}."}
        ]
    )
    
    print(f"repo name::{repo_name}")
    file_name = "/tmp/"+repo_name+"/generated_unit_tests.c"
    if response is not None:
        with open(file_name, 'w') as file:
            file.write(response.choices[0].message.content)
    
    print(f"Unit tests saved to {file_name}")
    return response



# Main logic to identify memory leaks and generate unit tests
def identify_and_generate_tests(folder_path, target_file,repo_name):
    # Step 1: List files in the directory
    try:
    # Step 2: Read the target file
        target_file_path = os.path.join(folder_path, target_file)
        #file_content = read_file(target_file_path)["content"]
        """ read_file_response=read_file(target_file_path)
        print("file content")
        print(read_file_response) """

        # Step 3: Generate unit tests for memory leaks
        response = generate_unit_tests(target_file_path,repo_name)
        print("Generated Unit Tests:")
        print(response)
        return True
    except Exception as e:
        print(f"Exception while generating test cases::\n\n{e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process repository details.")
    parser.add_argument("file_path", help="Path to the folder in the repository")
    args = parser.parse_args()
    read_file_content(args.file_path)
    # Define the arguments
    """ parser.add_argument("repo_name", help="Name of the repository")
    
    parser.add_argument("file_name", help="Name of the file to process")

    # Parse the arguments
    args = parser.parse_args()

    # step 1: generate test cases
    response=identify_and_generate_tests(folder_path=args.folder_path,target_file=args.file_name,repo_name=args.repo_name)
    if not response:
        sys.exit(1) """
