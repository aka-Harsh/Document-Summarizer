# backend/utils/file_handler.py

import os
import re
import json
import pickle
import io
from typing import Dict, Any, Optional, Union, List
import chardet
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileHandler:
    """
    Handles file I/O operations for the document summarizer.
    """
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """
        Read a text file and return its contents.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: File contents
        """
        # Get file extension
        ext = FileHandler.get_file_extension(file_path).lower()
        
        # Process based on file type
        if ext == '.pdf':
            return FileHandler.read_pdf(file_path)
        elif ext == '.docx':
            return FileHandler.read_docx(file_path)
        elif ext == '.html':
            return FileHandler.read_html(file_path)
        elif ext == '.md':
            return FileHandler.read_markdown(file_path)
        else:  # Default to regular text file
            try:
                # Detect file encoding
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding']
                
                # Read the file with the detected encoding
                logger.info(f"Reading text file with detected encoding: {encoding}")
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError as e:
                logger.error(f"Unicode decode error: {str(e)}")
                # Fallback to latin-1 which rarely fails
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error reading file: {str(e)}")
                return f"Error reading file: {str(e)}"
    
    @staticmethod
    def read_pdf(file_path: str) -> str:
        """
        Extract text from a PDF file with robust error handling.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text
        """
        try:
            # Try multiple libraries in case one fails
            text = ""
            
            # Try PyPDF2 first
            try:
                import PyPDF2
                logger.info("Trying to read PDF with PyPDF2")
                
                with open(file_path, 'rb') as file:
                    try:
                        pdf_reader = PyPDF2.PdfReader(file)
                        
                        # Extract text from each page
                        for page_num in range(len(pdf_reader.pages)):
                            try:
                                page = pdf_reader.pages[page_num]
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text + "\n\n"
                            except Exception as e:
                                logger.error(f"Error extracting text from page {page_num}: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error reading PDF with PyPDF2: {str(e)}")
            except ImportError:
                logger.error("PyPDF2 library not installed")
            
            # If PyPDF2 failed, try pdfplumber
            if not text.strip():
                try:
                    import pdfplumber
                    logger.info("Trying to read PDF with pdfplumber")
                    
                    with pdfplumber.open(file_path) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n\n"
                except ImportError:
                    logger.error("pdfplumber library not installed")
                except Exception as e:
                    logger.error(f"Error reading PDF with pdfplumber: {str(e)}")
            
            # If all attempts failed, try a simple binary read approach
            if not text.strip():
                logger.info("Using fallback binary read method")
                with open(file_path, 'rb') as file:
                    content = file.read()
                    
                    # Try to decode with various encodings
                    for encoding in ['utf-8', 'latin-1', 'ascii', 'cp1252']:
                        try:
                            text = content.decode(encoding, errors='replace')
                            if text:
                                break
                        except Exception:
                            continue
            
            # Clean the text
            if text:
                # Replace non-printable characters
                text = ''.join(char if ord(char) < 128 or char.isspace() else ' ' for char in text)
                
                # Clean up extra whitespace
                text = re.sub(r'\s+', ' ', text)
                text = re.sub(r'\n\s*\n', '\n\n', text)
                
                return text
            else:
                return "Could not extract text from PDF file."
        except Exception as e:
            logger.error(f"Unexpected error reading PDF: {str(e)}")
            return f"Error reading PDF: {str(e)}"
    
    @staticmethod
    def read_docx(file_path: str) -> str:
        """
        Extract text from a DOCX file.
        
        Args:
            file_path (str): Path to the DOCX file
            
        Returns:
            str: Extracted text
        """
        try:
            from docx import Document
            
            document = Document(file_path)
            text = ""
            
            for paragraph in document.paragraphs:
                text += paragraph.text + "\n"
            
            return text
        except ImportError:
            return "Error: python-docx library not installed. Please install it using 'pip install python-docx'."
        except Exception as e:
            logger.error(f"Error reading DOCX: {str(e)}")
            return f"Error reading DOCX: {str(e)}"
    
    @staticmethod
    def read_html(file_path: str) -> str:
        """
        Extract text from an HTML file.
        
        Args:
            file_path (str): Path to the HTML file
            
        Returns:
            str: Extracted text
        """
        try:
            import html2text
            
            # Read with error handling for encoding
            try:
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding'] or 'utf-8'
                html_content = raw_data.decode(encoding)
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    html_content = f.read()
            
            converter = html2text.HTML2Text()
            converter.ignore_links = True
            converter.ignore_images = True
            
            return converter.handle(html_content)
        except ImportError:
            return "Error: html2text library not installed. Please install it using 'pip install html2text'."
        except Exception as e:
            logger.error(f"Error reading HTML: {str(e)}")
            return f"Error reading HTML: {str(e)}"
    
    @staticmethod
    def read_markdown(file_path: str) -> str:
        """
        Read a Markdown file.
        
        Args:
            file_path (str): Path to the Markdown file
            
        Returns:
            str: File contents
        """
        try:
            # Read with error handling for encoding
            try:
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    result = chardet.detect(raw_data)
                    encoding = result['encoding'] or 'utf-8'
                return raw_data.decode(encoding)
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
        except Exception as e:
            logger.error(f"Error reading Markdown file: {str(e)}")
            return f"Error reading Markdown file: {str(e)}"
    
    @staticmethod
    def write_text_file(file_path: str, content: str) -> None:
        """
        Write content to a text file.
        
        Args:
            file_path (str): Path to the file
            content (str): Content to write
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @staticmethod
    def read_json_file(file_path: str) -> Dict[str, Any]:
        """
        Read a JSON file and return its contents.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            Dict[str, Any]: Parsed JSON content
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict[str, Any]) -> None:
        """
        Write data to a JSON file.
        
        Args:
            file_path (str): Path to the file
            data (Dict[str, Any]): Data to write
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def save_pickle(file_path: str, obj: Any) -> None:
        """
        Save an object to a pickle file.
        
        Args:
            file_path (str): Path to the file
            obj (Any): Object to save
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Save to pickle file
        with open(file_path, 'wb') as f:
            pickle.dump(obj, f)
    
    @staticmethod
    def load_pickle(file_path: str) -> Any:
        """
        Load an object from a pickle file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            Any: Loaded object
        """
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """
        Get the extension of a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            str: File extension
        """
        return os.path.splitext(file_path)[1].lower()
    
    @staticmethod
    def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
        """
        List all files in a directory, optionally filtered by extension.
        
        Args:
            directory (str): Directory path
            extension (Optional[str]): File extension to filter by
            
        Returns:
            List[str]: List of file paths
        """
        if not os.path.exists(directory):
            return []
        
        files = []
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                if extension is None or file.endswith(extension):
                    files.append(file_path)
        
        return files
    
    @staticmethod
    def ensure_directory(directory: str) -> None:
        """
        Ensure a directory exists.
        
        Args:
            directory (str): Directory path
        """
        os.makedirs(directory, exist_ok=True)