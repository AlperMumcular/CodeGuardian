import os
import shutil

def aggregate(result=""):
    report_dir = "reports"
    output_file = "document.md"

    # Check if report directory exists
    if not os.path.exists(report_dir):
        print(f"The directory '{report_dir}' does not exist.")
        return result

    # Walk through the directory tree and read .md files
    for root, dirs, files in os.walk(report_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as md_file:
                        result += md_file.read() + "\n\n"
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")

    # Write the aggregated result to document.md
    try:
        with open(output_file, 'w', encoding='utf-8') as output_md:
            output_md.write(result)
        print(f"Aggregated content written to '{output_file}'")
    except Exception as e:
        print(f"Error writing to '{output_file}': {e}")

    # Delete the 'report' folder
    try:
        shutil.rmtree(report_dir)
        print(f"Deleted '{report_dir}' folder.")
    except Exception as e:
        print(f"Error deleting '{report_dir}': {e}")

    return result

# Call the function
aggregated_result = aggregate()
