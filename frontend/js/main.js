/**
 * Main application logic for Document Summarizer
 * Connects the UI controller with the API service
 */

class App {
    constructor() {
        // Get DOM elements
        this.summarizeBtn = document.getElementById('summarize-btn');
        
        // Initialize the app
        this.init();
    }
    
    init() {
        // Add event listener for summarize button
        this.summarizeBtn.addEventListener('click', () => this.handleSummarize());
    }
    
    async handleSummarize() {
        // Validate input
        if (!window.uiController.validateInput()) {
            return;
        }
        
        // Show loading indicator
        window.uiController.showLoading();
        
        try {
            // Get options
            const options = window.uiController.getSummarizationOptions();
            
            // Get input and process accordingly
            const text = window.uiController.getInputText();
            const file = window.uiController.getUploadedFile();
            
            let result;
            
            if (text) {
                // Process text input
                result = await window.apiService.summarizeText(
                    text,
                    options.modelType,
                    options.ratio,
                    options.language
                );
            } else if (file) {
                // Process file input
                result = await window.apiService.summarizeFile(
                    file,
                    options.modelType,
                    options.ratio,
                    options.language
                );
            }
            
            // Hide loading indicator
            window.uiController.hideLoading();
            
            // Display results
            if (result) {
                window.uiController.displayResults(result);
            }
        } catch (error) {
            // Hide loading indicator
            window.uiController.hideLoading();
            
            // Show error message
            window.uiController.showError(error.message);
            console.error('Summarization error:', error);
        }
    }
}

// Wait for document to be ready before initializing app
document.addEventListener('DOMContentLoaded', () => {
    // The uiController and apiService should already be initialized by their respective files
    // and attached to the window object
    
    // Initialize app
    const app = new App();
});