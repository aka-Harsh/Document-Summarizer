/**
 * Theme Switcher for Document Summarizer
 * Manages dark/light mode switching and saves preferences to localStorage
 */

class ThemeSwitcher {
    constructor() {
        // DOM elements
        this.themeToggle = document.getElementById('theme-toggle');
        this.body = document.body;
        this.html = document.documentElement;
        
        // Local storage key
        this.storageKey = 'document-summarizer-theme';
        
        // Initialize
        this.init();
    }
    
    init() {
        console.log("Theme switcher initializing...");
        
        // Load saved theme preference or use system preference
        this.loadThemePreference();
        
        // Add event listener for toggle button
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
            console.log("Theme toggle button listener added");
        } else {
            console.error("Theme toggle button not found in the DOM");
        }
        
        // Listen for system theme changes
        this.listenForSystemThemeChanges();
    }
    
    loadThemePreference() {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem(this.storageKey);
        
        if (savedTheme) {
            // Apply saved theme
            console.log(`Applying saved theme: ${savedTheme}`);
            this.applyTheme(savedTheme);
        } else {
            // Use system preference
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            console.log(`No saved theme, using system preference: ${prefersDark ? 'dark' : 'light'}`);
            this.applyTheme(prefersDark ? 'dark' : 'light');
        }
    }
    
    applyTheme(theme) {
        if (theme === 'dark') {
            this.html.classList.add('dark');
            this.body.classList.add('dark');
            document.querySelector('html').style.backgroundColor = '#1a202c';
            console.log("Dark theme applied");
        } else {
            this.html.classList.remove('dark');
            this.body.classList.remove('dark');
            document.querySelector('html').style.backgroundColor = '';
            console.log("Light theme applied");
        }
    }
    
    toggleTheme() {
        console.log("Toggling theme");
        // Toggle dark class
        const isDark = this.html.classList.contains('dark');
        this.applyTheme(isDark ? 'light' : 'dark');
        
        // Save preference to localStorage
        const currentTheme = this.html.classList.contains('dark') ? 'dark' : 'light';
        localStorage.setItem(this.storageKey, currentTheme);
        console.log(`Theme preference saved: ${currentTheme}`);
    }
    
    listenForSystemThemeChanges() {
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            // Only apply if user hasn't set a preference
            if (!localStorage.getItem(this.storageKey)) {
                console.log("System theme changed, updating theme");
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
}

// Initialize theme switcher when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM loaded, initializing theme switcher");
    window.themeSwitcher = new ThemeSwitcher();
});