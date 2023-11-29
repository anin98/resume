# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import extract_and_process_pdf  # Import the processing function
import tempfile
import os

class UploadResumeAPIView(APIView):

    def post(self, request, *args, **kwargs):
        # Check if the file is part of the request
        if 'file' not in request.FILES:
            return Response({"error": "No file provided."}, status=400)

        uploaded_file = request.FILES['file']

        # Optional: Check if the uploaded file is a PDF
        if uploaded_file.content_type != 'application/pdf':
            return Response({"error": "File is not a PDF."}, status=400)

        # Optional: Check file size
        MAX_FILE_SIZE = 10485760  # 10 MB limit
        if uploaded_file.size > MAX_FILE_SIZE:
            return Response({"error": "File size exceeds limit."}, status=400)

        # Create a temporary file to save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            # Write the uploaded file content to the temporary file
            for chunk in uploaded_file.chunks():
                temp_pdf.write(chunk)
            temp_pdf_path = temp_pdf.name

        # Process the PDF and get JSON data
        try:
            json_data = extract_and_process_pdf(temp_pdf_path)
        except Exception as e:
            print(f"Error processing file: {e}")
            os.remove(temp_pdf_path)
            return Response({"error": "Error processing file."}, status=500)

        # Clean up: Delete the temporary file
        os.remove(temp_pdf_path)

        # Return JSON response
        return Response(json_data)
