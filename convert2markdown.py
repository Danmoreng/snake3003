import json

def json_to_markdown(file_path):
    # Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Helper function to adjust heading levels in the message content
    def adjust_headings(content):
        lines = content.split('\n')
        adjusted_lines = []
        for line in lines:
            # Increase the level of markdown headings by adding an extra '#'
            if line.startswith('#'):
                adjusted_lines.append('#' + line)
            else:
                adjusted_lines.append(line)
        return '\n'.join(adjusted_lines)

    # Helper function to process each message
    def process_message(message_id):
        node = data["mapping"][message_id]
        markdown = ""

        # Check if there's a valid message to process
        if "message" in node and node["message"] and "content" in node["message"]:
            # Determine the author
            author = "User" if node["message"]["author"]["role"] == "user" else "Assistant"

            # Get and adjust the message content
            content = node["message"]["content"]["parts"][0]
            content = adjust_headings(content)
            markdown += f"### {author}:\n{content}\n\n"

        # Recursively process any child messages
        if "children" in node:
            for child_id in node["children"]:
                markdown += process_message(child_id)

        return markdown

    # Find the root node (the one without a parent and with children)
    root_id = None
    for key, value in data["mapping"].items():
        if "parent" in value and value["parent"] is None and "children" in value:
            root_id = key
            break

    # Generate Markdown from the root node
    if root_id:
        return process_message(root_id)
    else:
        return "No root message found."

# Specify the path to the JSON file
file_path = 'chat.json'

# Convert to Markdown
markdown_output = json_to_markdown(file_path)

# Save the output to a Markdown file
with open('ChatGPTConversation.md', 'w') as md_file:
    md_file.write(markdown_output)

print("Markdown file 'ChatGPTConversation.md' has been created successfully.")
