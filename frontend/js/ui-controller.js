/**
 * UI Controller for Document Summarizer
 * Manages UI interactions, form handling, and display updates
 */

class UIController {
    constructor() {
        // Store DOM elements
        this.elements = {
            // Tabs
            inputTabs: document.getElementById('input-tabs'),
            textTab: document.getElementById('text-tab'),
            fileTab: document.getElementById('file-tab'),
            textInput: document.getElementById('text-input'),
            fileInput: document.getElementById('file-input'),
            
            // Form inputs
            inputText: document.getElementById('input-text'),
            fileUpload: document.getElementById('file-upload'),
            fileInfo: document.getElementById('file-info'),
            fileName: document.getElementById('file-name'),
            removeFile: document.getElementById('remove-file'),
            modelType: document.getElementById('model-type'),
            summaryRatio: document.getElementById('summary-ratio'),
            ratioValue: document.getElementById('ratio-value'),
            language: document.getElementById('language'),
            
            // Buttons
            summarizeBtn: document.getElementById('summarize-btn'),
            copyBtn: document.getElementById('copy-btn'),
            downloadBtn: document.getElementById('download-btn'),
            
            // Results
            resultsSection: document.getElementById('results-section'),
            summaryText: document.getElementById('summary-text'),
            originalLength: document.getElementById('original-length'),
            summaryLength: document.getElementById('summary-length'),
            compressionRatio: document.getElementById('compression-ratio'),
            processingTime: document.getElementById('processing-time'),
            
            // Loading
            loadingIndicator: document.getElementById('loading-indicator')
        };
        
        // File data
        this.uploadedFile = null;
        
        // Initialize UI
        this.init();
    }
    
    init() {
        // Set up tabs
        this.setupTabs();
        
        // Set up range slider
        this.setupRangeSlider();
        
        // Set up file upload
        this.setupFileUpload();
        
        // Set up result actions
        this.setupResultActions();
    }
    
    setupTabs() {
        // Add click listeners to tabs
        this.elements.textTab.addEventListener('click', () => this.switchTab('text-input'));
        this.elements.fileTab.addEventListener('click', () => this.switchTab('file-input'));
    }
    
    switchTab(tabId) {
        // Update tab buttons
        const tabs = this.elements.inputTabs.querySelectorAll('button');
        tabs.forEach(tab => {
            if (tab.dataset.tab === tabId) {
                tab.classList.add('text-blue-600', 'dark:text-blue-400', 'border-blue-600', 'dark:border-blue-400');
                tab.classList.remove('text-gray-500', 'dark:text-gray-400', 'border-transparent');
                tab.setAttribute('aria-selected', 'true');
            } else {
                tab.classList.remove('text-blue-600', 'dark:text-blue-400', 'border-blue-600', 'dark:border-blue-400');
                tab.classList.add('text-gray-500', 'dark:text-gray-400', 'border-transparent');
                tab.setAttribute('aria-selected', 'false');
            }
        });
        
        // Show active tab content, hide others
        const tabPanes = document.querySelectorAll('.tab-pane');
        tabPanes.forEach(pane => {
            if (pane.id === tabId) {
                pane.classList.remove('hidden');
                pane.classList.add('active');
            } else {
                pane.classList.add('hidden');
                pane.classList.remove('active');
            }
        });
    }
    
    setupRangeSlider() {
        // Update ratio value display when slider changes
        this.elements.summaryRatio.addEventListener('input', (e) => {
            this.elements.ratioValue.textContent = `${e.target.value}%`;
        });
    }
    
    setupFileUpload() {
        // Listen for file selection
        this.elements.fileUpload.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFileSelection(e.target.files[0]);
            }
        });
        
        // Handle drag and drop
        const dropZone = this.elements.fileUpload.parentElement;
        
        // Prevent default behavior for drag events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, e => {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });
        
        // Add visual feedback for drag events
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('drag-over');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('drag-over');
            }, false);
        });
        
        // Handle dropped files
        dropZone.addEventListener('drop', e => {
            if (e.dataTransfer.files.length > 0) {
                this.handleFileSelection(e.dataTransfer.files[0]);
            }
        }, false);
        
        // Remove file button
        if (this.elements.removeFile) {
            this.elements.removeFile.addEventListener('click', () => {
                this.uploadedFile = null;
                this.elements.fileUpload.value = '';
                this.elements.fileInfo.classList.add('hidden');
            });
        }
    }
    
    handleFileSelection(file) {
        // Check file size
        const maxSize = 10 * 1024 * 1024; // 10MB
        if (file.size > maxSize) {
            alert('File is too large. Maximum size is 10MB.');
            return;
        }
        
        // Check file type
        const validTypes = ['.txt', '.pdf', '.docx', '.html', '.md'];
        const fileExt = file.name.substring(file.name.lastIndexOf('.'));
        
        if (!validTypes.includes(fileExt.toLowerCase())) {
            alert('Invalid file type. Please upload a TXT, PDF, DOCX, HTML, or MD file.');
            return;
        }
        
        // Store file and update UI
        this.uploadedFile = file;
        this.elements.fileName.textContent = file.name;
        this.elements.fileInfo.classList.remove('hidden');
    }
    
    setupResultActions() {
        // Copy summary to clipboard
        if (this.elements.copyBtn) {
            this.elements.copyBtn.addEventListener('click', () => {
                const summaryText = this.elements.summaryText.textContent;
                
                if (summaryText) {
                    navigator.clipboard.writeText(summaryText)
                        .then(() => {
                            // Show success animation
                            this.elements.copyBtn.firstElementChild.classList.add('copy-success');
                            setTimeout(() => {
                                this.elements.copyBtn.firstElementChild.classList.remove('copy-success');
                            }, 1000);
                        })
                        .catch(err => {
                            console.error('Failed to copy text: ', err);
                            alert('Failed to copy to clipboard');
                        });
                }
            });
        }
        
        // Download summary
        if (this.elements.downloadBtn) {
            this.elements.downloadBtn.addEventListener('click', () => {
                const summaryText = this.elements.summaryText.textContent;
                
                if (summaryText) {
                    const blob = new Blob([summaryText], { type: 'text/plain' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    
                    a.href = url;
                    a.download = 'summary.txt';
                    a.click();
                    
                    URL.revokeObjectURL(url);
                }
            });
        }
    }
    
    getInputText() {
        // Get text from active input method
        if (this.elements.textInput && !this.elements.textInput.classList.contains('hidden')) {
            return this.elements.inputText.value.trim();
        }
        
        return null;
    }
    
    getUploadedFile() {
        // Get uploaded file if file tab is active
        if (this.elements.fileInput && !this.elements.fileInput.classList.contains('hidden')) {
            return this.uploadedFile;
        }
        
        return null;
    }
    
    getSummarizationOptions() {
        // Get options from form
        return {
            modelType: this.elements.modelType.value,
            ratio: parseInt(this.elements.summaryRatio.value) / 100,
            language: this.elements.language.value
        };
    }
    
    validateInput() {
        // Check if we have valid input
        const text = this.getInputText();
        const file = this.getUploadedFile();
        
        if (!text && !file) {
            // No input provided
            alert('Please enter text or upload a file to summarize.');
            return false;
        }
        
        return true;
    }
    
    showLoading() {
        // Show loading indicator
        this.elements.loadingIndicator.classList.remove('hidden');
    }
    
    hideLoading() {
        // Hide loading indicator
        this.elements.loadingIndicator.classList.add('hidden');
    }
    
    displayResults(result) {
        // Update summary text
        this.elements.summaryText.textContent = result.summary;
        
        // Update statistics
        this.elements.originalLength.textContent = `${result.original_length} words`;
        this.elements.summaryLength.textContent = `${result.summary_length} words`;
        this.elements.compressionRatio.textContent = `${(result.compression_ratio * 100).toFixed(1)}%`;
        this.elements.processingTime.textContent = `${result.processing_time.toFixed(2)}s`;
        
        // Show results section with animation
        this.elements.resultsSection.classList.remove('hidden');
        this.elements.resultsSection.classList.add('fade-in');
        
        // Scroll to results
        this.elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    showError(message) {
        // Hide loading indicator
        this.hideLoading();
        
        // Show error message
        alert(`Error: ${message}`);
    }
}

// Create global UI controller instance
window.uiController = new UIController();