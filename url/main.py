from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from .hackathon import get_local_file_and_content, get_github_file_and_content
import os
from dotenv import load_dotenv
from on_device_requests import get_response_on_device
from aggregate import aggregate, delete_results

load_dotenv()

# Set up Claude API
api_claude = os.getenv('LLM_TOKEN')
Claude_model = ChatAnthropic(
    model_name="claude-3-haiku-20240307",
    temperature=0,
    api_key=api_claude
)

# Template for vulnerability analysis
template = "{code}\nProvide a vulnerability report for the given code."

# Function to create the reports folder structure
def create_reports_folder(file_path, base_folder):
    report_path = os.path.join(base_folder, file_path)
    report_dir = os.path.dirname(report_path)

    # Ensure the directory exists
    os.makedirs(report_dir, exist_ok=True)

    return report_path

# Function to generate vulnerability report
def analyze_code_with_claude(file_path, content, reports_base):
    try:
        # Prepare the prompt
        prompt = template.format(code=content)

        # Get response from Claude
        response = Claude_model.invoke(prompt)
        #response=get_response_on_device(prompt)

        # Save the report as a Markdown file maintaining the folder structure
        relative_path = file_path.replace(os.path.sep, "/")
        report_file = create_reports_folder(relative_path + ".md", reports_base)

        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"# Vulnerability Report for `{file_path}`\n\n")
            f.write("## Code Snippet\n")
            f.write(f"```{os.path.splitext(file_path)[1][1:]}\n{content}\n```\n\n")
            f.write("## Vulnerability Analysis\n")
            f.write(response.content)

        print(f"Report generated: {report_file}")
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")

# Main function to integrate local or GitHub content
def main():
    # Delete results folder if it exists
    delete_results()

    source_type = input("Choose source type (local/github): ").strip().lower()

    try:
        # Fetch file content and folder structure
        if source_type == "local":
            folder_path = input("Enter the local folder path: ").strip()
            folder_structure, file_content_dict = get_local_file_and_content(folder_path)
        elif source_type == "github":
            repo_url = input("Enter the GitHub repository URL: ").strip()
            folder_structure, file_content_dict = get_github_file_and_content(repo_url)
        else:
            print("Invalid source type. Please choose either 'local' or 'github'.")
            return

        # Print the folder structure
        print("Folder Structure:")
        print(folder_structure)

        # Create a base reports folder
        reports_base = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_base, exist_ok=True)

        # Analyze each file's content using Claude
        for file_path, content in file_content_dict.items():
            print(f"Analyzing {file_path}...")
            analyze_code_with_claude(file_path, content, reports_base)
        
        document = aggregate()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
