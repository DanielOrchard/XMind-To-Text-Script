import xmindparser
import os
import sys

xmind_file_path = ""

if len(sys.argv) > 1:
    xmind_file_path = sys.argv[1]
    print(f"File path received: {xmind_file_path}")

# xmind_file_path = r"D:\Dev\Repo\Mindmap_Quizzer\Cardiovascular Pharmacology.xmind"
xmind_content = xmindparser.xmind_to_dict(xmind_file_path)

def format_hierarchy(data, indent=0):
    formatted_text = ""
    indent_str = "    " * indent  # Define the indentation string
    
    if isinstance(data, list):
        for item in data:
            if 'topic' in item:  # Adjusting for the presence of 'topic' key in the list items
                formatted_text += format_hierarchy(item['topic'], indent)
            else:
                formatted_text += format_hierarchy(item, indent)
    elif isinstance(data, dict):
        # Replace newlines in the title with a space
        title = data.get('title', 'Untitled').replace("\n", " ")
        formatted_text += f"{indent_str}- {title}\n"
        
        # Directly accessing 'topics' from the current dict if it exists
        children = data.get('topics', [])
        for child in children:
            formatted_text += format_hierarchy(child, indent + 1)
    
    return formatted_text

# Assuming xmind_content is the list that wraps the main topic dict
formatted_hierarchy = format_hierarchy(xmind_content)  # Directly passing the xmind_content

# Generate the output file name based on the input XMind file name
base_name = os.path.basename(xmind_file_path)  # Extracts the file name with extension
output_file_name = os.path.splitext(base_name)[0] + "_hierarchy.txt"  # Replaces the extension

# Generate the full path for the output file, assuming you want it in the same directory
output_file_path = os.path.join(os.path.dirname(xmind_file_path), output_file_name)

# Write the formatted text to the output file
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(formatted_hierarchy)
