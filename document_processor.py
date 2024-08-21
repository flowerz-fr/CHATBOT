import fitz  # PyMuPDF
import re
import os

class DocumentProcessor:
    def __init__(self, source: str):
        self.source = source
        self.doc = self.get_pdf_file()
        self.toc_index = None
        self.references_index = None
        self.page_content = []

    def get_pdf_file(self):
        """Open the PDF file using PyMuPDF."""
        return fitz.open(self.source)

    def merge_lines_content(self, lines):
        """Merge lines where a line does not end with a period and the next starts with a lowercase letter."""
        merged_lines = []
        i = 0
        while i < len(lines):
            if i < len(lines) - 1 and not lines[i].endswith('.') and lines[i+1][0].islower():
                merged_lines.append(lines[i] + ' ' + lines[i+1])
                i += 2
            else:
                merged_lines.append(lines[i])
                i += 1
        return merged_lines
    
    def find_toc_index(self):
        """Find the index of the Table of Contents (TOC) in the first two pages."""
        for page_num in range(2):
            page = self.doc[page_num].get_text()
            lines = [line for line in page.split('\n') if line.strip()]
            toc_index = next((i for i, line in enumerate(lines) if re.search(r"TABLES DES MATIERES|TABLE DES MATIERES|Table des matières", line)), None)
            if toc_index is not None:
                return toc_index
        return None

    def find_title(self, lines, start_index, end_index):
        """Find and return the document title."""
        if not lines[end_index].startswith(("Page", "PAGE", "P1")):
            title = lines[start_index+1:end_index-1]
        else:
            title = lines[start_index+1:end_index]
        return " ".join(title)

    def process_document_body(self):
        """Process the body content of the document."""
        self.toc_index = self.find_toc_index()
        
        for page in self.doc:
            text = page.get_text()
            lines = [line for line in text.split('\n') if line.strip() and '\uf0b7' not in line and '\uf0fe' not in line]
            lines = [re.sub(r'\.{6,}', '.....', line) for line in lines]

            self.references_index = next((i for i, line in enumerate(lines) if re.match(r"ELH-\d{4}-\d{6}(?:_\d{1})?", line)), len(lines))
            
            if self.toc_index is not None:
                content = lines[self.toc_index:self.references_index]
            else:
                content = lines[:self.references_index]

            while True:
                new_content = self.merge_lines_content(content)
                if new_content == content:
                    break
                content = new_content 

            self.page_content.extend(content)

        return "\n".join(self.page_content)

    def process_document_information(self):
        """Extract and process document information from the PDF."""
        self.toc_index = self.find_toc_index()

        page = self.doc[0].get_text()
        lines = [line for line in page.split('\n') if line.strip()]

        self.references_index = next((i for i, line in enumerate(lines) if re.match(r"ELH-\d{4}-\d{6}(?:_\d{1})?", line)), None)
        compte_rendu_index = next((i for i, line in enumerate(lines) if re.match(r"\bCOMPTE[-\s]RENDU\b", line)), None)

        info_content = lines[:self.toc_index] + lines[self.references_index:]
        title = self.find_title(info_content, compte_rendu_index, compte_rendu_index + 3)

        version = next((line for line in info_content if re.match(r"(\d\.\d)", line)), None)
        date = next((line for line in info_content if re.match(r"\b\d{2}/\d{2}/\d{4}\b", line)), "01/01/0001")
        confidentiality = next((line for line in info_content if re.match(r"(Diffusion (?:Limitée|Normale) Orano|Confidentiel Orano)", line)), None)
        perimeter = os.path.basename(os.path.dirname(self.source))
        investigation_number = os.path.basename(self.source).split(".")[0]

        metadata = {
            "Title": title,
            "Version": version,
            "Date": date,
            "Confidentiality": confidentiality,
            "Perimeter": perimeter,
            "Investigation Number": investigation_number,
            "Source": self.source
        }
        return metadata

    def process_document(self):
        """Process the entire document, returning metadata and page content."""
        metadata = self.process_document_information()
        page_content = self.process_document_body()
        return {
            "metadata": metadata,
            "page_content": page_content
        }

# Example:

# To process a single PDF document
# processor = DocumentProcessor('path/to/the/document.pdf')
# document_data = processor.process_document()
