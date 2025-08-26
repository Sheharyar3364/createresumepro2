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
