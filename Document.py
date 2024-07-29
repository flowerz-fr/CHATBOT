import fitz  # PyMuPDF
import re
import os
import base64

class Document:
    def __init__(self, source: str):
        self.source = source
        self.doc = self.get_pdf_file()
        self.toc_index = None
        self.references_index = None
        self.page_content = []
        self.base64_images = self.extract_images_from_pdf_to_base64()
        
        
    
    def get_pdf_file(self):
        doc = fitz.open(self.source)
        return doc
    
    # def add_hyperlink_to_figure_lines(self, lines):
    #     """Add hyperlinks to lines containing the word 'Figure' followed by a number."""
    #     figure_pattern = re.compile(r"Figure \d+")
    #     linked_lines = []
    #     for line in lines:
    #         if figure_pattern.search(line):
    #             # Modify this line to include a hyperlink (example format)
    #             line = f'<a href="#figure"></a>{line}'
    #         linked_lines.append(line)
    #     return linked_lines
    # --------------------------------------------------------
    
    def extract_images_from_pdf_to_base64(self):
        base64_strings_img = []

        # Open the PDF file
        pdf_file = self.doc
        
        # Iterate over each page in the PDF
        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            image_list = page.get_images(full=True)
            
            # Iterate over each image in the page
            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                
                # Encode the image bytes to base64
                base64_string = base64.b64encode(image_bytes).decode('utf-8')
                base64_strings_img.append(base64_string)
        
        # Remove duplicate base64 strings
        base64_strings_img = list(set(base64_strings_img))
        
        return base64_strings_img
    
    # --------------------------------------------------------

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
        toc_index = None
        for page_num in range(2):
            page = self.doc[page_num].get_text()
            lines = page.split('\n')
            lines = [line for line in lines if line.strip()]
            toc_index = next((i for i, line in enumerate(lines) if "TABLES DES MATIERES" in line or "TABLE DES MATIERES" in line or "Table des matières" in line), None)
            if toc_index is not None:
                break
        return toc_index
    
    
    def find_title(self, lines, start_index, end_index):
        title = "Title not found"
        if not lines[end_index].startswith(("Page", "PAGE", "P1")):
            title = lines[start_index+1:end_index-1]
            title = " ".join(title)
        else:
            title = lines[start_index+1:end_index]
            title = " ".join(title)
        return title



    def process_document_body(self):
        self.toc_index = self.find_toc_index()
        
        for page in self.doc:
            # Get text from the page
            text = page.get_text()
            
            # Split text into lines and remove empty lines
            lines = text.split('\n')
            lines = [line for line in lines if line.strip()]
            lines = [line for line in lines if '\uf0b7' not in line]
            lines = [line for line in lines if '\uf0fe' not in line]

            def replace_dots(line):
                return re.sub(r'\.{6,}', '.....', line)

            lines = [replace_dots(line) for line in lines]

            # Find the index where the references start
            self.references_index = next((i for i, line in enumerate(lines) if re.match(r"ELH-\d{4}-\d{6}(?:_\d{1})?", line)), len(lines))
            
            if self.toc_index is not None:
                content = lines[self.toc_index:self.references_index]
            else:
                content = lines[:self.references_index]
            
            # content = self.add_hyperlink_to_figure_lines(content)

            # Merge lines content
            while True:
                new_content = self.merge_lines_content(content)
                if new_content == content:
                    break
                content = new_content 

            self.page_content.extend(content)

        page_content = "\n".join(self.page_content)
        # page_content = " ".join(self.page_content)
        return page_content

    def process_document_information(self):
        self.toc_index = self.find_toc_index()

        page = self.doc[0].get_text()
        lines = page.split('\n')
        lines = [line for line in lines if line.strip()]

        # Find the index where the references start
        self.references_index = next((i for i, line in enumerate(lines) if re.match(r"ELH-\d{4}-\d{6}(?:_\d{1})?", line)), None)

        # Find the index of the line that contains the word "COMPTE-RENDU"
        compte_rendu_index = next((i for i, line in enumerate(lines) if re.match(r"\bCOMPTE[-\s]RENDU\b", line)), None)

        info_content = lines[:self.toc_index] + lines[self.references_index:]
        title = self.find_title(info_content, compte_rendu_index, compte_rendu_index + 3)

        version = None
        for line in info_content:
            if re.match(r"(\d\.\d)", line):
                version = line
                break

        date = None
        for line in info_content:
            if re.match(r"\b\d{2}/\d{2}/\d{4}\b", line):
                date = line
                break
            
        # If no date was found, set it to "01/01/0001"
        if date is None:
            date = "01/01/0001"

        confidentiality = None
        for line in info_content:
            if re.match(r"(Diffusion (?:Limitée|Normale) Orano|Confidentiel Orano)", line):
                confidentiality = line
                break

        perimeter = os.path.basename(os.path.dirname(self.source))
        investigation_number = os.path.basename(self.source).split(".")[0]
        source = self.source

        metadata = {
            "Title": title,
            "Version": version,
            "Date": date,
            "Confidentiality": confidentiality,
            "Perimeter": perimeter,
            "Investigation Number": investigation_number,
            "Source": source,
            "images_base64": self.base64_images
        }
        return metadata

    def process_document(self):
        metadata = self.process_document_information()
        page_content = self.process_document_body()
        document = {
            "metadata": metadata,
            "page_content": page_content
        }
        return document