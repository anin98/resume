import os
import openai
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
import json

def parse_response_to_json(structured_response):
    # Custom parser logic goes here
    # Placeholder logic - modify as per your response format
    json_data = {}
    lines = structured_response.split('\n')
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            json_data[key.strip()] = value.strip()
    return json_data

def extract_and_process_pdf(pdf_file_path):
    # Load environment variables
    load_dotenv()

    # Extract text from PDF
    text = extract_text(pdf_file_path)

    # Load OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Refine this prompt to get a better-formatted response
    prompt = "Format the following information into structured JSON data:\n\n" + text

    # Send text to OpenAI API for processing
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024
    )

    structured_response = response.choices[0].text.strip()

    # Attempt to parse the response as JSON
    try:
        json_data = json.loads(structured_response)
    except json.JSONDecodeError:
        json_data = parse_response_to_json(structured_response)

    return json_data

# Example usage
pdf_file = '/Users/anindita/Desktop/untitled folder/mahmudul_cv - K. M. Mahmudul Haque.pdf'
json_data = extract_and_process_pdf(pdf_file)

# Saving the structured data to output.json
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=4)

print("Data saved to output.json")
