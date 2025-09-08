# Script to clean emoji characters from mock_data_generator.py
import re

def clean_emojis(file_path):
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace common emojis with >>>
    emojis_to_replace = ['🌟', '🏢', '🔗', '💼', '🧠', '🎯', '📄', '🎉', '📊', '⚠️', '💾']
    for emoji in emojis_to_replace:
        content = content.replace(emoji, '>>>')
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Cleaned emojis from {file_path}")

if __name__ == "__main__":
    clean_emojis('mock_data_generator.py')