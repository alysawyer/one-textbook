from pdfminer.high_level import extract_text

def pdf_to_text(pdf_file, txt_file):
    text = extract_text(pdf_file)
    with open(txt_file, 'w') as f:
        f.write(text)

pdf_to_text('(Lingua Latina per se Illustrata) Hans H. Ørberg - Pars I_ Familia Romana-Focus Publishing_R. Pullins Co. (2003).pdf', 'output.txt')
