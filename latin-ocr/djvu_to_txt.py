import fitz  # PyMuPDF

def extract_text_from_djvu(djvu_filename, txt_filename):
    # Open the DJVU file
    doc = fitz.open(djvu_filename)

    # Initialize an empty text variable to store the extracted text
    text = ""

    # Iterate through each page in the DJVU document
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Extract text from the current page
        page_text = page.get_text()

        # Append the extracted text to the overall text
        text += page_text

    # Close the DJVU document
    doc.close()

    # Write the extracted text to a text file
    with open(txt_filename, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)

if __name__ == "__main__":
    djvu_file = "input.djvu"  # Replace with the path to your DJVU file
    txt_file = "text1/output.txt"  # Replace with the desired output text file path

    extract_text_from_djvu(djvu_file, txt_file)
    print(f"Text extracted from '{djvu_file}' and saved to '{txt_file}'.")
