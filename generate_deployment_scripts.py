from openai import OpenAI
import os
import sys
import argparse


client = OpenAI()

# Function to generate deployment scripts based on README
def generate_scripts_from_readme(readme_content,folder_name):
    prompt = f"""
    You are an expert DevOps assistant. Based on the provided README content, your task is to generate the following scripts:
    
    1. A Dockerfile to set up a containerized environment for a C/C++ project. 
       - It should install all necessary dependencies for building and testing the project.
       - Include Valgrind tool to detect memory leaks.
    
    2. A shell script `build_and_test.sh` that:
       -Build the Docker image using the Dockerfile.
       -Run a Docker container to execute the unit tests.
       -Use Valgrind to check for memory leaks during the test execution.
       -After the tests are executed, copy the test result logs or any relevant files from the container back to the {folder_name} folder on the host machine for review.
       -Clean up the Docker image and container after execution
    
    3. A Makefile that includes targets for building and running the tests.


    Please generate the required scripts based on the project description and dependencies mentioned in the README.
    """
    user_promt='''Here is the README content:
    
            ```markdown
            {readme_content}
            ```

            Please generate the required scripts based on the project description and dependencies mentioned in the README'''
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            {"role": "assistant","content":"provide me readme file content based on which I will generate the required scripts"},
            {"role":"user","content":user_promt}
        ]
    )

    return response['choices'][0]['message']['content']

def generate_deployment_scripts(folder_path,repo_name):

# Example usage
    try:
        readme_path = folder_path+"/README.md"
        with open(readme_path, 'r') as file:
            readme_content = file.read()

        print(readme_content)

        scripts = generate_scripts_from_readme(readme_content)

        # Save the generated scripts to files
        with open("./tmp/"+repo_name+"Dockerfile", "w") as dockerfile:
            dockerfile.write(scripts.split("```dockerfile")[1].split("```")[0].strip())

        with open("./tmp/"+repo_name+"build_and_test.sh", "w") as shell_script:
            shell_script.write(scripts.split("```bash")[1].split("```")[0].strip())

        with open("./tmp/"+repo_name+"Makefile", "w") as makefile:
            makefile.write(scripts.split("```makefile")[1].split("```")[0].strip())

        print("Scripts generated successfully!")
        return True
    except Exception as e:
        print(f"Exception while generating deployment scripts")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process repository details.")

    # Define the arguments
    parser.add_argument("repo_name", help="Name of the repository")
    parser.add_argument("folder_path", help="Path to the folder in the repository")

    # Parse the arguments
    args = parser.parse_args()

    # Parse the arguments
    response=generate_deployment_scripts(folder_path=args.folder_path,repo_name=args.repo_name)
    if not response:
        sys.exit(1)