import fitz

def summarize_pdf(file_path):
    pdf = fitz.open(file_path)
    text = "".join([page.get_text() for page in pdf])
    return text[:1000] + "... (summary)"