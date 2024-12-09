from openai import OpenAI
import os
import sys
import argparse


client = OpenAI()

# Function to generate deployment scripts based on README
def generate_scripts_from_readme(readme_content, folder_name,repo_path):
    prompt = f"""
    You are an expert DevOps assistant. Based on the provided README content, your task is to generate the following scripts:
    
    1. A Dockerfile to set up a containerized environment for a C/C++ project. 
       - It should install all necessary dependencies for building and testing the project.
       - The code that needs to be executed on docker will be at folder {repo_path}. Use this code checkoit to copy to docker.
       - Include Valgrind tool to detect memory leaks.
    
    2. A shell script `build_and_test.sh` that:
       - Build the Docker image using the Dockerfile.
       - Run a Docker container to execute the unit tests.
       - Use Valgrind to check for memory leaks during the test execution.
       - After the tests are executed, copy the test result logs or any relevant files from the container back to the {folder_name} folder on the host machine for review and name the file as memory_leak.log.
       - Clean up the Docker image and container after execution.
    
    3. A Makefile that includes targets for building and running the tests. memory_leak_unit_test.c will be the unit test file and this file will be in the folder {repo_path}.Only this test case needs to be run.
       -'build','test',clean'
    
    Ensure the code blocks in your response use the following format:
    - Dockerfile: `Dockerfile`
    - Shell script: `bash`
    - Makefile: `Makefile

    Please generate the required scripts based on the project description and dependencies mentioned in the README.
    """
    user_prompt = f"""Here is the README content:
    
            ```markdown
            {readme_content}
            ```
            
            Please generate the required scripts based on the project description and dependencies mentioned in the README."""
    
    response = client.chat.completions.create(
        model="gpt-4",  # Ensure you're using the correct model here
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "Please provide me the README file content based on which I will generate the required scripts"},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_deployment_scripts(folder_path, repo_name):
    try:
        readme_path = os.path.join(folder_path, "README.md")
        
        # Read README file content
        with open(readme_path, 'r') as file:
            readme_content = file.read()

        # Generate scripts from the README content
        scripts = generate_scripts_from_readme(readme_content, './tmp/' + repo_name,folder_path)
        print(scripts)

        # Ensure that the response contains the expected code blocks
        if scripts:
            dockerfile_content = extract_code_block(scripts, "Dockerfile")
            shell_script_content = extract_code_block(scripts, "bash")
            makefile_content = extract_code_block(scripts, "Makefile")
            
            if dockerfile_content:
                # Save the generated scripts to files
                os.makedirs(f"./tmp/{repo_name}", exist_ok=True)
                with open(f"./tmp/{repo_name}/Dockerfile", "w") as dockerfile:
                    dockerfile.write(dockerfile_content)
            if shell_script_content:
                with open(f"./tmp/{repo_name}/build_and_test.sh", "w") as shell_script:
                    shell_script.write(shell_script_content)
            if makefile_content:
                with open(f"./tmp/{repo_name}/Makefile", "w") as makefile:
                    makefile.write(makefile_content)

                print("Scripts generated successfully!")
                return True
            else:
                print("Error: Could not find one or more required code blocks.")
                return False
        else:
            print("Error: No script content generated.")
            return False
    except Exception as e:
        print(f"Exception while generating deployment scripts: {e}")
        return False

def extract_code_block(response_content, block_type):
    try:
        start_marker = f"```{block_type}"
        end_marker = "```"
        
        if start_marker in response_content and end_marker in response_content:
            start_index = response_content.index(start_marker) + len(start_marker)
            end_index = response_content.index(end_marker, start_index)
            return response_content[start_index:end_index].strip()
        else:
            return None
    except Exception as e:
        print(f"Error extracting {block_type} block: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process repository details.")

    # Define the arguments
    parser.add_argument("folder_path", help="Name of the repository folder")
    parser.add_argument("repo_name", help="Name of the repository")

    # Parse the arguments
    args = parser.parse_args()

    print(f"path: {args.folder_path}")
    response = generate_deployment_scripts(folder_path=args.folder_path, repo_name=args.repo_name)
    if not response:
        sys.exit(1)
