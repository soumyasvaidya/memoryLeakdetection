import json
from openai import OpenAI
import argparse
import os

client = OpenAI()

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
    },
    {
        "name": "write_to_file",  # Tool for writing to a file
        "description": "Write content to the specified file path.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to write to."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file."
                }
            },
            "required": ["file_path", "content"],
            "additionalProperties": False
        }
    }
]

def append_test_cases(unit_test_file_path, info_file_path, final_response):
    """
    Separates code content and explanations from the response and writes them to different files.
    
    Args:
        unit_test_file_path (str): Path to the file where test case code will be stored.
        info_file_path (str): Path to the file where additional information will be stored.
        final_response (Response): The model's response containing test cases and explanations.
    """
    # Extract test cases from the model response
    test_cases_content = final_response.choices[0].message.content

    # Separate code content from explanations/comments
    code_parts = []
    info_parts = []
    in_code_block = False

    for line in test_cases_content.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            code_parts.append(line)
        else:
            info_parts.append(line)

    # Join the extracted parts
    code_content = "\n".join(code_parts).strip()
    info_content = "\n".join(info_parts).strip()

    # Write the code content to the test cases file
    with open(unit_test_file_path, 'w') as code_file:
        code_file.write(code_content)
    
    # Write the additional information to the info file
    with open(info_file_path, 'w') as info_file:
        info_file.write(info_content)
    
    print(f"Code written to {unit_test_file_path}")
    print(f"Additional information written to {info_file_path}")


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def handle_tool_call(response, repo_path):
    tool_call = response.choices[0].message.tool_calls[0]
    print("Tool call initiated:", tool_call)

    arguments = json.loads(tool_call.function.arguments)
    file_path = os.path.join(repo_path, arguments.get('file_path'))

    if tool_call.function.name == "read_file":
        file_content = read_file(file_path)
        # Prepare function call result message for read_file
        function_call_result_message = {
            "role": "tool",
            "content": json.dumps({
                "file_path": file_path,
                "file_content": file_content
            }),
            "tool_call_id": tool_call.id
        }
    elif tool_call.function.name == "write_to_file":
        content = arguments.get('content')
        result_message = write_to_file(file_path, content)
        function_call_result_message = {
            "role": "tool",
            "content": json.dumps({
                "file_path": file_path,
                "result": result_message
            }),
            "tool_call_id": tool_call.id
        }
    return function_call_result_message

def write_to_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Content successfully written to {file_path}"
    except Exception as e:
        return f"Error writing to file {file_path}: {e}"

def process_patch(patch_content, repo_path,repo_name):
    tools = [{"type": "function", "function": function_signatures[0]},
             {"type": "function", "function": function_signatures[1]}]  # Added write_to_file tool

    # Initial interaction
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are assisting with code analysis. Use the supplied tools to assist the user."},
            {"role": "user", "content": f"Analyze the patch and get required files:\n{patch_content}"}
        ],
        tools=tools
    )
    print(response)
    if response.choices[0].message.tool_calls:
        print("Processing tool calls...")

        tool_call_result_message = handle_tool_call(response, repo_path)

        # Update with the function call results
        completion_payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for analyzing patches."},
                {"role": "user", "content": "Please analyze and generate test cases from the patch."},
                {"role": "user","content": "I have provided the code file before the memory leak fix was applied. The patch provided shows the changes that were made to fix memory leaks in the code. Please analyze the code before the fix and generate test cases that reproduce the memory leaks present in this version of the code. Specifically, the test cases should: \n\n1. Focus on the parts of the code where memory is allocated but not freed, or where memory is not properly cleaned up. \n2. Simulate real-world usage scenarios that would trigger the memory leak in the pre-fix version. \n4. Include mock functions or dependencies where necessary, especially if external resources such as files or DB access or services are involved. \n5. The test cases should include assertions that check for memory leaks, and use a test framework like `unittest`. \n6. Ensure edge cases, such as failed memory allocations, are tested."},
                {"role": response.choices[0].message.role, "content": "What should be the output format."},
                {"role": "user", "content": "Given the patch file, generate executable unit tests in .c format with specific input values and expected assertions for reproducing the memory leak.Any additional reposne should be added as comments"},
                response.choices[0].message,
                tool_call_result_message
            ],
            "tools": tools  # Retaining tools here for next tool calls
        }

        # Final step to provide test cases
        final_response = client.chat.completions.create(
            model=completion_payload["model"],
            messages=completion_payload["messages"],
            tools=completion_payload["tools"]
        )

        print("Generated test cases:")
        print(final_response)
        append_test_cases("./tmp/"+repo_name+"/unit_case.c", "./tmp/"+repo_name+"/unit_test_case_details.txt",final_response)
        return final_response

    else:
        print("No tool calls were necessary.")
        return response

# Main Entry
parser = argparse.ArgumentParser(description="Process repository details.")
parser.add_argument("file_path", help="Path to the folder in the repository")
parser.add_argument("folder_path", help="Path to the folder in the repository")
parser.add_argument("repo_name", help="Path to the folder in the repository")

args = parser.parse_args()

patch_file_path = args.file_path
with open(patch_file_path, 'r') as patch_file:
    patch_content = patch_file.read()

process_patch(patch_content, args.folder_path,args.repo_name)
