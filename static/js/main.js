/**
 * TakoTech Website - Main JavaScript
 * Enhanced user interactions and functionality
 */

// Global TakoTech namespace
window.TakoTech = {
    // Configuration
    config: {
        apiBaseUrl: '/api/v1/',
        animationDuration: 300,
        debounceDelay: 300
    },
    
    // Utility functions
    utils: {
        // Debounce function
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Format numbers with Persian digits
        formatPersianNumber: function(num) {
            const persianDigits = '۰۱۲۳۴۵۶۷۸۹';
            return num.toString().replace(/\d/g, (digit) => persianDigits[digit]);
        },
        
        // Show loading spinner
        showLoading: function(element) {
            const spinner = document.createElement('div');
            spinner.className = 'spinner mx-auto';
            spinner.id = 'loading-spinner';
            element.innerHTML = '';
            element.appendChild(spinner);
        },
        
        // Hide loading spinner
        hideLoading: function(element) {
            const spinner = element.querySelector('#loading-spinner');
            if (spinner) {
                spinner.remove();
            }
        },
        
        // Show toast notification
        showToast: function(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `fixed top-4 left-4 z-50 p-4 rounded-lg text-white max-w-sm alert-${type} animate-fade-in-up`;
            toast.innerHTML = `
                <div class="flex items-center">
                    <i class="fas fa-${this.getToastIcon(type)} ml-2"></i>
                    <span>${message}</span>
                    <button class="mr-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            
            document.body.appendChild(toast);
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 5000);
        },
        
        // Get toast icon based on type
        getToastIcon: function(type) {
            const icons = {
                success: 'check-circle',
                warning: 'exclamation-triangle',
                error: 'times-circle',
                info: 'info-circle'
            };
            return icons[type] || icons.info;
        },
        
        // Animate counter
        animateCounter: function(element, start, end, duration = 2000) {
            const startTime = performance.now();
            const animate = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const current = Math.floor(start + (end - start) * progress);
                
                element.textContent = this.formatPersianNumber(current);
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                }
            };
            requestAnimationFrame(animate);
        }
    },
    
    // Search functionality
    search: {
        init: function() {
            const searchInput = document.querySelector('#search-input');
            const searchResults = document.querySelector('#search-results');
            
            if (searchInput && searchResults) {
                searchInput.addEventListener('input', TakoTech.utils.debounce((e) => {
                    this.performSearch(e.target.value, searchResults);
                }, TakoTech.config.debounceDelay));
            }
        },
        
        performSearch: function(query, resultsContainer) {
            if (query.length < 2) {
                resultsContainer.innerHTML = '';
                resultsContainer.classList.add('hidden');
                return;
            }
            
            TakoTech.utils.showLoading(resultsContainer);
            resultsContainer.classList.remove('hidden');
            
            fetch(`/products/ajax/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    this.displaySearchResults(data.results, resultsContainer);
                })
                .catch(error => {
                    console.error('Search error:', error);
                    resultsContainer.innerHTML = '<div class="p-4 text-red-600">خطا در جستجو</div>';
                });
        },
        
        displaySearchResults: function(results, container) {
            if (results.length === 0) {
                container.innerHTML = '<div class="p-4 text-gray-600">نتیجه‌ای یافت نشد</div>';
                return;
            }
            
            const html = results.map(result => `
                <a href="/products/${result.slug}/" class="block p-4 hover:bg-gray-100 border-b">
                    <div class="font-medium text-gray-900">${result.name}</div>
                    <div class="text-sm text-gray-600">${result.category}</div>
                </a>
            `).join('');
            
            container.innerHTML = html;
        }
    },
    
    // Product interactions
    products: {
        // Track product view
        trackView: function(productSlug) {
            fetch(`/products/ajax/product/${productSlug}/view/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const viewCountElement = document.querySelector('.view-count');
                    if (viewCountElement) {
                        viewCountElement.textContent = TakoTech.utils.formatPersianNumber(data.view_count);
                    }
                }
            })
            .catch(error => console.error('View tracking error:', error));
        },
        
        // Track product download
        trackDownload: function(productSlug) {
            fetch(`/products/ajax/product/${productSlug}/download/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    TakoTech.utils.showToast('دانلود با موفقیت ثبت شد', 'success');
                }
            })
            .catch(error => console.error('Download tracking error:', error));
        },
        
        // Get CSRF token
        getCSRFToken: function() {
            return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                   document.querySelector('meta[name=csrf-token]')?.getAttribute('content') || '';
        }
    },
    
    // Form handling
    forms: {
        // Initialize all forms
        init: function() {
            document.querySelectorAll('form[data-ajax]').forEach(form => {
                form.addEventListener('submit', this.handleAjaxSubmit.bind(this));
            });
        },
        
        // Handle AJAX form submission
        handleAjaxSubmit: function(event) {
            event.preventDefault();
            
            const form = event.target;
            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin ml-2"></i>در حال ارسال...';
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    TakoTech.utils.showToast(data.message || 'عملیات با موفقیت انجام شد', 'success');
                    form.reset();
                } else {
                    TakoTech.utils.showToast(data.error || 'خطا در انجام عملیات', 'error');
                }
            })
            .catch(error => {
                console.error('Form submission error:', error);
                TakoTech.utils.showToast('خطا در ارسال فرم', 'error');
            })
            .finally(() => {
                // Restore button state
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            });
        },
        
        // Validate form fields
        validateField: function(field) {
            const value = field.value.trim();
            const type = field.type;
            const required = field.hasAttribute('required');
            
            let isValid = true;
            let errorMessage = '';
            
            if (required && !value) {
                isValid = false;
                errorMessage = 'این فیلد الزامی است';
            } else if (type === 'email' && value && !this.isValidEmail(value)) {
                isValid = false;
                errorMessage = 'ایمیل وارد شده معتبر نیست';
            } else if (type === 'tel' && value && !this.isValidPhone(value)) {
                isValid = false;
                errorMessage = 'شماره تلفن وارد شده معتبر نیست';
            }
            
            this.showFieldError(field, isValid ? null : errorMessage);
            return isValid;
        },
        
        // Show field error
        showFieldError: function(field, message) {
            const errorElement = field.parentElement.querySelector('.field-error');
            
            if (message) {
                if (errorElement) {
                    errorElement.textContent = message;
                } else {
                    const error = document.createElement('div');
                    error.className = 'field-error text-red-600 text-sm mt-1';
                    error.textContent = message;
                    field.parentElement.appendChild(error);
                }
                field.classList.add('border-red-500');
            } else {
                if (errorElement) {
                    errorElement.remove();
                }
                field.classList.remove('border-red-500');
            }
        },
        
        // Email validation
        isValidEmail: function(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        },
        
        // Phone validation (Iranian format)
        isValidPhone: function(phone) {
            return /^(\+98|0)?9\d{9}$/.test(phone.replace(/\s/g, ''));
        }
    },
    
    // Animation helpers
    animations: {
        // Fade in on scroll
        fadeInOnScroll: function() {
            const elements = document.querySelectorAll('[data-animate="fade-in"]');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-fade-in-up');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });
            
            elements.forEach(element => observer.observe(element));
        },
        
        // Counter animation
        animateCounters: function() {
            const counters = document.querySelectorAll('[data-counter]');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const element = entry.target;
                        const end = parseInt(element.dataset.counter);
                        const start = 0;
                        
                        TakoTech.utils.animateCounter(element, start, end);
                        observer.unobserve(element);
                    }
                });
            }, { threshold: 0.5 });
            
            counters.forEach(counter => observer.observe(counter));
        }
    },
    
    // Initialize everything
    init: function() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.initializeComponents();
            });
        } else {
            this.initializeComponents();
        }
    },
    
    // Initialize all components
    initializeComponents: function() {
        this.search.init();
        this.forms.init();
        this.animations.fadeInOnScroll();
        this.animations.animateCounters();
        
        // Track page view for products
        const productSlug = document.body.dataset.productSlug;
        if (productSlug) {
            this.products.trackView(productSlug);
        }
        
        console.log('TakoTech website initialized successfully');
    }
};

// Initialize TakoTech
TakoTech.init();

// Global event listeners
document.addEventListener('click', function(e) {
    // Close dropdowns when clicking outside
    if (!e.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.add('hidden');
        });
    }
    
    // Handle download buttons
    if (e.target.closest('[data-download]')) {
        e.preventDefault();
        const productSlug = e.target.closest('[data-download]').dataset.download;
        TakoTech.products.trackDownload(productSlug);
    }
});

// Handle escape key for modals and dropdowns
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // Close modals
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
        
        // Close dropdowns
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.add('hidden');
        });
    }
});

// Export for global access
window.TakoTech = TakoTech;
