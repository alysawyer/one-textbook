import PyPDF2

def extract_text_from_pdf(pdf_file, txt_file):
    try:
        # Open the PDF file in read-binary mode
        with open(pdf_file, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Initialize an empty string to store the extracted text
            text = ""

            # Iterate through each page in the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Get the text content of the page
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            
            # Write the extracted text to the output TXT file
            with open(txt_file, 'w', encoding='utf-8') as txt_file:
                txt_file.write(text)
            
            print(f"Text extracted and saved to {txt_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    pdf_file = "cover_letter_lowe.pdf"  # Replace with the path to your PDF file
    txt_file = "output.txt"   # Replace with the desired output text file name

    extract_text_from_pdf(pdf_file, txt_file)
