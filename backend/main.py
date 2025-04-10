# backend/main.py

import os
import argparse
import logging
from typing import Dict, Any

from model.summarizer import DocumentSummarizer
from utils.file_handler import FileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_arg_parser() -> argparse.ArgumentParser:
    """
    Set up command line argument parser.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(description='Document Summarization Tool')
    
    # Input and output file arguments
    parser.add_argument(
        '-i', '--input',
        type=str,
        help='Path to the input document'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Path to save the summary'
    )
    parser.add_argument(
        '-d', '--directory',
        type=str,
        help='Path to a directory of documents to summarize'
    )
    
    # Summarization parameters
    parser.add_argument(
        '-m', '--model',
        type=str,
        choices=['textrank', 'tfidf', 'ensemble'],
        default='ensemble',
        help='Summarization model to use'
    )
    parser.add_argument(
        '-r', '--ratio',
        type=float,
        default=0.3,
        help='Target ratio of summary to original text length'
    )
    parser.add_argument(
        '-l', '--language',
        type=str,
        default='english',
        help='Language of the input document'
    )
    
    # Model management
    parser.add_argument(
        '--save-model',
        type=str,
        help='Path to save the trained model'
    )
    parser.add_argument(
        '--load-model',
        type=str,
        help='Path to a saved model to load'
    )
    
    # API mode
    parser.add_argument(
        '--api',
        action='store_true',
        help='Run in API mode with FastAPI server'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port to run the API server on'
    )
    
    return parser

def summarize_file(
    file_path: str,
    output_path: str,
    summarizer: DocumentSummarizer,
    ratio: float
) -> Dict[str, Any]:
    """
    Summarize a single file.
    
    Args:
        file_path (str): Path to the input file
        output_path (str): Path to save the summary
        summarizer (DocumentSummarizer): Configured summarizer instance
        ratio (float): Target ratio of summary to original text length
        
    Returns:
        Dict[str, Any]: Summary results
    """
    # Read the input file
    logger.info(f"Reading file: {file_path}")
    text = FileHandler.read_text_file(file_path)
    
    # Generate summary
    logger.info(f"Generating summary using {summarizer.model_type} model")
    result = summarizer.summarize(text, ratio=ratio)
    
    # Save the summary if output path is provided
    if output_path:
        logger.info(f"Saving summary to: {output_path}")
        FileHandler.write_text_file(output_path, result['summary'])
    
    return result

def summarize_directory(
    directory: str,
    output_dir: str,
    summarizer: DocumentSummarizer,
    ratio: float
) -> Dict[str, Dict[str, Any]]:
    """
    Summarize all text files in a directory.
    
    Args:
        directory (str): Path to the directory of input files
        output_dir (str): Path to save the summaries
        summarizer (DocumentSummarizer): Configured summarizer instance
        ratio (float): Target ratio of summary to original text length
        
    Returns:
        Dict[str, Dict[str, Any]]: Summary results for each file
    """
    # Ensure output directory exists
    if output_dir:
        FileHandler.ensure_directory(output_dir)
    
    # Get all text files in the directory
    text_extensions = ['.txt', '.md', '.rst', '.html', '.xml']
    all_files = []
    for ext in text_extensions:
        all_files.extend(FileHandler.list_files(directory, ext))
    
    if not all_files:
        logger.warning(f"No text files found in {directory}")
        return {}
    
    # Process each file
    results = {}
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        output_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_summary.txt") if output_dir else None
        
        try:
            result = summarize_file(file_path, output_path, summarizer, ratio)
            results[file_name] = result
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
    
    return results

def main():
    """
    Main entry point for the application.
    """
    # Parse command line arguments
    parser = setup_arg_parser()
    args = parser.parse_args()
    
    # Check if running in API mode
    if args.api:
        from api.app import start_api_server
        logger.info(f"Starting API server on port {args.port}")
        start_api_server(port=args.port)
        return
    
    # Initialize summarizer
    summarizer = DocumentSummarizer(model_type=args.model, language=args.language)
    
    # Load model if specified
    if args.load_model:
        logger.info(f"Loading model from {args.load_model}")
        summarizer.load_model(args.load_model)
    
    # Process input
    if args.input:
        # Summarize a single file
        result = summarize_file(args.input, args.output, summarizer, args.ratio)
        
        # Print summary info
        print("\n--- SUMMARY ---")
        print(result['summary'])
        print("\n--- STATISTICS ---")
        print(f"Original length: {result['original_length']} words")
        print(f"Summary length: {result['summary_length']} words")
        print(f"Compression ratio: {result['compression_ratio']:.2f}")
    
    elif args.directory:
        # Summarize all files in a directory
        results = summarize_directory(args.directory, args.output, summarizer, args.ratio)
        
        # Print summary info
        print(f"\nProcessed {len(results)} files")
        for file_name, result in results.items():
            print(f"\n--- {file_name} ---")
            print(f"Original length: {result['original_length']} words")
            print(f"Summary length: {result['summary_length']} words")
            print(f"Compression ratio: {result['compression_ratio']:.2f}")
    
    else:
        # No input specified
        logger.error("No input specified. Use --input or --directory")
        parser.print_help()
    
    # Save model if specified
    if args.save_model:
        logger.info(f"Saving model to {args.save_model}")
        summarizer.save_model(args.save_model)

if __name__ == "__main__":
    main()