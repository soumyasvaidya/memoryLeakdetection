from openai import OpenAI
import os

client = OpenAI()

# Function to validate if the memory leak issue reproduced by unit tests matches the fix
def validate_memory_leak(log_content, code_content, unit_test_content, fixed_code_content):
    prompt = f"""
    You are a skilled assistant in memory leak validation and debugging. Your task is to verify if the memory leak issue reproduced by the unit tests is identical to the issue fixed in the provided code.

    ### Input:
    1. **Memory Leak Log File**: A report of the memory leak issue, including error messages and where the leak occurred in the original code.
    2. **Original Code File (with Memory Leaks)**: The original version of the code where the memory leak occurred.
    3. **Fixed Code File**: The updated version of the code with the memory leak fixed.
    4. **Generated Unit Test File**: Unit test cases generated to validate the fixed code and ensure the memory leak issue does not occur.

    ### Task:
    - Review the memory leak log to understand where the memory leak occurred.
    - Compare the original code and the fixed code to identify what changes were made to resolve the memory leak.
    - Review the unit test cases to check if they test the affected parts of the code and verify that the memory leak is fixed.
    - Confirm if the memory leak reproduced by the unit tests matches the fixed issue.

    ### Output:
    - A simple "Yes" or "No" answer:
       - **"Yes"**: If the memory leak reproduced by the unit tests is identical to the memory leak fixed in the code.
       - **"No"**: If the memory leak reproduced by the unit tests is not the same as the issue fixed in the code.

    Please provide a "Yes" or "No" answer.
    """

    # Send the prompt to OpenAI API for processing
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert in debugging and memory leak validation."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "Provide Memory Leak Logs."},
            {"role": "user", "content": log_content},
            {"role": "assistant", "content": "Provide original Code File (with Memory Leaks)"},
            {"role": "user", "content": code_content},
            {"role": "assistant", "content": "Provide Fixed Code File"},
            {"role": "user", "content": fixed_code_content},
            {"role": "assistant", "content": "Provide Generated Unit Test File"},
            {"role": "user", "content": unit_test_content}

        ]
    )

    # Get the result from LLM response
    result = response['choices'][0]['message']['content']
    print(f"LLM Result: {result}")

    # Return the result of validation (Yes or No)
    return result.strip().lower()

# Example usage
def main(log_file_path,code_file_path,unit_test_file_path,fixed_code_file_path):
    
    # Read log content
    with open(log_file_path, "r") as log_file:
        log_content = log_file.read()

    # Read the fixed code content
    with open(code_file_path, "r") as code_file:
        code_content = code_file.read()

    # Read the unit test content
    with open(unit_test_file_path, "r") as unit_test_file:
        unit_test_content = unit_test_file.read()

    # Read the fixed code content again (same file as the original code)
    with open(fixed_code_file_path, "r") as fixed_code_file:
        fixed_code_content = fixed_code_file.read()

    # Validate if the unit test case reproduces the memory leak correctly
    result = validate_memory_leak(log_content, code_content, unit_test_content, fixed_code_content)
    
    # Check the result and print if the leak was successfully validated or not
    if result == "yes":
        print("Memory leak issue reproduced successfully and fixed correctly!")
        return 0
    else:
        print("Memory leak issue not reproduced correctly by the unit tests. Please check the tests.")
        return -1
        # Re-prompt logic can be added here if necessary.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process repository details.")

    # Define the arguments
    parser.add_argument("log_file_path", help="path to the log file")
    parser.add_argument("code_file_path", help="Path to the code file with memory leaks")
    parser.add_argument("unit_test_file_path", help="path to the log file")
    parser.add_argument("fixed_code_file_path", help="Path to the code file with fix for memory leaks")


    # Parse the arguments
    args = parser.parse_args()
    main(args.log_file_path,args.code_file_path,args.unit_test_file_path,args.fixed_code_file_path)
