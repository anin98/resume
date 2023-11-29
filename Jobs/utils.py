import os
import openai
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
import json

def parse_response_to_json(structured_response):
    # Custom parser logic to convert structured text into JSON
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

    # Define the prompt for OpenAI's API
    prompt = "Format the following information into structured JSON data:\n\n" + text

    # Send text to OpenAI API for processing
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024
        )
        structured_response = response.choices[0].text.strip()
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return {"error": "Error processing text with OpenAI."}

    # Attempt to parse the response as JSON
    try:
        json_data = json.loads(structured_response)
    except json.JSONDecodeError:
        json_data = parse_response_to_json(structured_response)

    return json_data
