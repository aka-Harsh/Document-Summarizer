/**
 * API Service for Document Summarizer
 * Handles all API communication with the backend
 */

class ApiService {
    constructor() {
        // API base URL - change this to match your backend URL
        this.baseUrl = 'http://localhost:8000';
        console.log("API Service initialized with base URL:", this.baseUrl);
    }
    
    /**
     * Summarize text using the API
     * 
     * @param {string} text - Text to summarize
     * @param {string} modelType - Type of summarization model
     * @param {number} ratio - Target ratio of summary to original text
     * @param {string} language - Language of the text
     * @returns {Promise<Object>} - Promise that resolves to the summary result
     */
    async summarizeText(text, modelType = 'ensemble', ratio = 0.3, language = 'english') {
        console.log("Summarizing text with model:", modelType, "ratio:", ratio);
        try {
            const response = await fetch(`${this.baseUrl}/summarize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text,
                    model_type: modelType,
                    ratio,
                    language
                })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error summarizing text:', error);
            throw error;
        }
    }
    
    /**
     * Summarize a file using the API
     * 
     * @param {File} file - File to summarize
     * @param {string} modelType - Type of summarization model
     * @param {number} ratio - Target ratio of summary to original text
     * @param {string} language - Language of the text
     * @returns {Promise<Object>} - Promise that resolves to the summary result
     */
    async summarizeFile(file, modelType = 'ensemble', ratio = 0.3, language = 'english') {
        console.log("Summarizing file:", file.name, "with model:", modelType, "ratio:", ratio);
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('model_type', modelType);
            formData.append('ratio', ratio);
            formData.append('language', language);
            
            const response = await fetch(`${this.baseUrl}/summarize/file`, {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error summarizing file:', error);
            throw error;
        }
    }
    
    /**
     * Get available models
     * 
     * @returns {Promise<Array<string>>} - Promise that resolves to array of model types
     */
    async getAvailableModels() {
        try {
            const response = await fetch(`${this.baseUrl}/models`);
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting available models:', error);
            throw error;
        }
    }
    
    /**
     * Get model information
     * 
     * @param {string} modelType - Type of model to get info for
     * @param {string} language - Language of the model
     * @returns {Promise<Object>} - Promise that resolves to model information
     */
    async getModelInfo(modelType, language = 'english') {
        try {
            const response = await fetch(`${this.baseUrl}/models/${modelType}?language=${language}`);
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error getting model info:', error);
            throw error;
        }
    }
    
    /**
     * Benchmark models on text
     * 
     * @param {string} text - Text to benchmark
     * @param {number} ratio - Target ratio of summary to original text
     * @param {string} language - Language of the text
     * @returns {Promise<Object>} - Promise that resolves to benchmark results
     */
    async benchmarkModels(text, ratio = 0.3, language = 'english') {
        try {
            const response = await fetch(`${this.baseUrl}/benchmark`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text,
                    ratio,
                    language
                })
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error benchmarking models:', error);
            throw error;
        }
    }
}

// Create global API service instance
window.apiService = new ApiService();
console.log("API Service attached to window object");