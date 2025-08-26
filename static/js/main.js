<<<<<<< HEAD
// Main JavaScript for CreateProResume

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // File upload handling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const label = document.querySelector(`label[for="${e.target.id}"]`);
            
            if (file) {
                // Check file size (16MB limit)
                if (file.size > 16 * 1024 * 1024) {
                    alert('File size must be less than 16MB');
                    e.target.value = '';
                    return;
                }
                
                // Update label with filename
                if (label) {
                    label.textContent = file.name;
                    label.classList.add('text-success');
                }
            }
        });
    });

    // Referral code copy functionality
    const copyReferralBtn = document.getElementById('copyReferralCode');
    if (copyReferralBtn) {
        copyReferralBtn.addEventListener('click', function() {
            const referralCode = document.getElementById('referralCode').textContent;
            navigator.clipboard.writeText(referralCode).then(function() {
                // Show success message
                const originalText = copyReferralBtn.textContent;
                copyReferralBtn.textContent = 'Copied!';
                copyReferralBtn.classList.remove('btn-outline-primary');
                copyReferralBtn.classList.add('btn-success');
                
                setTimeout(function() {
                    copyReferralBtn.textContent = originalText;
                    copyReferralBtn.classList.remove('btn-success');
                    copyReferralBtn.classList.add('btn-outline-primary');
                }, 2000);
            }).catch(function(err) {
                console.error('Could not copy text: ', err);
                alert('Failed to copy referral code. Please copy it manually.');
            });
        });
    }

    // Order status update confirmation
    const statusUpdateForms = document.querySelectorAll('.status-update-form');
    statusUpdateForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const newStatus = form.querySelector('select[name="status"]').value;
            if (newStatus === 'completed' || newStatus === 'delivered') {
                if (!confirm(`Are you sure you want to mark this order as ${newStatus}? This will notify the customer.`)) {
                    e.preventDefault();
                }
            }
        });
    });

    // Auto-hide flash messages
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        if (!message.classList.contains('alert-danger')) {
            setTimeout(() => {
                const alert = new bootstrap.Alert(message);
                alert.close();
            }, 5000);
        }
    });

    // Enhanced order search functionality
    const orderSearch = document.getElementById('orderSearch');
    if (orderSearch) {
        orderSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const orderCards = document.querySelectorAll('.order-card');
            
            orderCards.forEach(card => {
                const orderText = card.textContent.toLowerCase();
                if (orderText.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Pricing calculator
    const serviceSelect = document.getElementById('serviceType');
    if (serviceSelect) {
        serviceSelect.addEventListener('change', function() {
            const selectedService = this.value;
            const prices = {
                'basic': 99,
                'standard': 199,
                'premium': 299
            };
            
            const priceDisplay = document.getElementById('priceDisplay');
            if (priceDisplay && prices[selectedService]) {
                priceDisplay.textContent = `$${prices[selectedService]}`;
            }
        });
    }

    // Form validation enhancements
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Dashboard statistics animation
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        let currentValue = 0;
        const increment = finalValue / 50;
        
        const timer = setInterval(() => {
            currentValue += increment;
            if (currentValue >= finalValue) {
                currentValue = finalValue;
                clearInterval(timer);
            }
            stat.textContent = Math.floor(currentValue);
        }, 20);
    });

    // Mobile menu handling
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on a link
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }
});

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        const alert = new bootstrap.Alert(alertDiv);
        alert.close();
    }, 5000);
}
=======
// Main JavaScript for Professional Resume Writing Service

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFormValidation();
    initializePricingUpdates();
    initializeFileUploads();
    initializeTooltips();
    initializeSmoothScrolling();
    
    // Add loading states to buttons
    addLoadingStates();
});

// Form Validation Enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Add real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                clearFieldError(this);
            });
        });
        
        // Enhanced form submission
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showValidationErrors();
            } else {
                addFormLoadingState(this);
            }
        });
    });
}

// Field validation
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';
    
    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    
    // Email validation
    if (fieldName === 'email' && value) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address';
        }
    }
    
    // Phone validation
    if (fieldName === 'phone' && value) {
        const phonePattern = /^[\+]?[1-9][\d]{0,15}$/;
        if (!phonePattern.test(value.replace(/\s|-|\(|\)/g, ''))) {
            isValid = false;
            errorMessage = 'Please enter a valid phone number';
        }
    }
    
    // Name validation
    if ((fieldName === 'first_name' || fieldName === 'last_name') && value) {
        if (value.length < 2) {
            isValid = false;
            errorMessage = 'Name must be at least 2 characters long';
        }
    }
    
    // Show/hide error
    if (!isValid) {
        showFieldError(field, errorMessage);
    } else {
        clearFieldError(field);
    }
    
    return isValid;
}

// Show field error
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-circle me-1"></i>${message}`;
    
    field.parentNode.appendChild(errorDiv);
}

// Clear field error
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Validate entire form
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Show validation errors notification
function showValidationErrors() {
    showNotification('Please correct the errors below', 'error');
    
    // Scroll to first error
    const firstError = document.querySelector('.is-invalid');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstError.focus();
    }
}

// Pricing Updates
function initializePricingUpdates() {
    const serviceTypeSelect = document.getElementById('service_type');
    const serviceTierSelect = document.getElementById('service_tier');
    
    if (serviceTypeSelect && serviceTierSelect) {
        serviceTypeSelect.addEventListener('change', updatePricing);
        serviceTierSelect.addEventListener('change', updatePricing);
        
        // Initial update
        updatePricing();
    }
}

// Update pricing display
function updatePricing() {
    const serviceType = document.getElementById('service_type')?.value;
    const serviceTier = document.getElementById('service_tier')?.value;
    
    if (!serviceType || !serviceTier) return;
    
    // This function is defined in the template with server data
    if (typeof window.updatePricing === 'function') {
        window.updatePricing();
    }
}

// File Upload Enhancement
function initializeFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            handleFileUpload(this);
        });
        
        // Add drag and drop functionality
        const container = input.closest('.mb-4, .mb-5');
        if (container) {
            addDragDropToContainer(container, input);
        }
    });
}

// Handle file upload
function handleFileUpload(input) {
    const files = input.files;
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    let hasErrors = false;
    
    Array.from(files).forEach(file => {
        // Check file size
        if (file.size > maxSize) {
            showFieldError(input, `File "${file.name}" is too large. Maximum size is 16MB.`);
            hasErrors = true;
        }
        
        // Check file type
        if (!allowedTypes.includes(file.type)) {
            showFieldError(input, `File "${file.name}" is not a valid format. Only PDF and DOCX files are allowed.`);
            hasErrors = true;
        }
    });
    
    if (!hasErrors) {
        clearFieldError(input);
        showFilePreview(input);
    }
}

// Show file preview
function showFilePreview(input) {
    const files = input.files;
    let previewContainer = input.parentNode.querySelector('.file-preview');
    
    // Remove existing preview
    if (previewContainer) {
        previewContainer.remove();
    }
    
    if (files.length > 0) {
        previewContainer = document.createElement('div');
        previewContainer.className = 'file-preview mt-2';
        
        Array.from(files).forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item d-flex align-items-center p-2 bg-light rounded mb-1';
            
            const icon = file.type === 'application/pdf' ? 'fa-file-pdf text-danger' : 'fa-file-word text-primary';
            const size = formatFileSize(file.size);
            
            fileItem.innerHTML = `
                <i class="fas ${icon} me-2"></i>
                <div class="flex-grow-1">
                    <div class="fw-medium">${file.name}</div>
                    <small class="text-muted">${size}</small>
                </div>
                <i class="fas fa-check-circle text-success"></i>
            `;
            
            previewContainer.appendChild(fileItem);
        });
        
        input.parentNode.appendChild(previewContainer);
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Add drag and drop functionality
function addDragDropToContainer(container, input) {
    container.addEventListener('dragover', function(e) {
        e.preventDefault();
        container.classList.add('drag-over');
    });
    
    container.addEventListener('dragleave', function(e) {
        e.preventDefault();
        container.classList.remove('drag-over');
    });
    
    container.addEventListener('drop', function(e) {
        e.preventDefault();
        container.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        input.files = files;
        handleFileUpload(input);
    });
    
    // Add drag-drop styling
    if (!document.getElementById('dragDropStyles')) {
        const style = document.createElement('style');
        style.id = 'dragDropStyles';
        style.textContent = `
            .drag-over {
                border: 2px dashed var(--primary-color) !important;
                background-color: rgba(30, 64, 175, 0.05) !important;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipElements.forEach(element => {
        new bootstrap.Tooltip(element);
    });
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add loading states to buttons
function addLoadingStates() {
    const buttons = document.querySelectorAll('button[type="submit"], .btn[type="submit"]');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.disabled) {
                addButtonLoadingState(this);
            }
        });
    });
}

// Add loading state to button
function addButtonLoadingState(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Processing...
    `;
    
    // Reset after 30 seconds as fallback
    setTimeout(() => {
        button.disabled = false;
        button.innerHTML = originalText;
    }, 30000);
}

// Add loading state to form
function addFormLoadingState(form) {
    form.classList.add('loading');
    
    const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
    if (submitButton) {
        addButtonLoadingState(submitButton);
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0# thoughts
I need to create a professional resume writing service platform using Flask and PostgreSQL. The application should have:

1. A homepage with hero section, service descriptions, and 3-tier pricing
2. Order form with file uploads for resumes/cover letters
3. Stripe payment integration
4. Admin dashboard for order management
5. Email notifications
6. Professional styling with the specified color scheme

I'll use the Flask guidelines provided and implement a clean, production-ready application with proper database models, secure file handling, and responsive design.

# useful_guidelines_from_blueprints
From flask_website blueprint:
- Listen on port 5000
- Use werkzeug.security generate_password_hash with default method
- Never hard-code foreign keys
- Avoid JSON APIs, favor server-side rendering
- Use Bootstrap for UI components
- Set secret_key as: app.secret_key = os.environ.get("SESSION_SECRET")

From flask_stripe blueprint:
- Integrate with Stripe-hosted checkout page
- Use STRIPE_SECRET_KEY environment variable
- Redirect to Stripe checkout session

# directory_structure
```json
[
    {"path": "app.py", "status": "new"},
    {"path": "main.py", "status": "new"},
    {"path": "models.py", "status": "new"},
    {"path": "routes.py", "status": "new"},
    {"path": "forms.py", "status": "new"},
    {"path": "config.py", "status": "new"},
    {"path": "templates/base.html", "status": "new"},
    {"path": "templates/index.html", "status": "new"},
    {"path": "templates/order.html", "status": "new"},
    {"path": "templates/admin/login.html", "status": "new"},
    {"path": "templates/admin/dashboard.html", "status": "new"},
    {"path": "templates/success.html", "status": "new"},
    {"path": "templates/cancel.html", "status": "new"},
    {"path": "static/css/style.css", "status": "new"},
    {"path": "static/js/main.js", "status": "new"},
    {"path": "uploads/.gitkeep", "status": "new"}
]
>>>>>>> ded7f2e4447248a018f7dd7d09de9c43eb09fa0d
