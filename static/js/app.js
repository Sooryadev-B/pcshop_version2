/* Overclock PC Shop - Main Global Interactions Script */

// Debounce utility for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle utility for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize deals countdown timer
    initCountdownTimer();

    // 2. Highlight active navbar link
    highlightActiveNavbarLink();

    // 3. Smooth animated scroll triggers
    initScrollAnimations();

    // 4. Quick buy indicators
    initQuickBuyClickHandlers();

    // 5. Add smooth page load animation
    addPageLoadAnimation();

    // 6. Enhanced button interactions
    initButtonInteractions();

    // 7. Improved form interactions
    initFormInteractions();

    // 8. Accessibility improvements
    initAccessibilityFeatures();
});

// Add page load fade-in effect
function addPageLoadAnimation() {
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.style.opacity = '0';
        mainContent.style.animation = 'fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards';
    }
}

// Enhanced Countdown Timer with better styling
function initCountdownTimer() {
    const countdownEl = document.getElementById('deal-countdown');
    if (!countdownEl) return;

    const endDateAttr = countdownEl.dataset.endDate;
    const targetDate = endDateAttr ? new Date(endDateAttr) : (() => {
        const fallback = new Date();
        fallback.setDate(fallback.getDate() + 2);
        fallback.setHours(fallback.getHours() + 4);
        return fallback;
    })();

    const updateTimer = () => {
        const now = new Date().getTime();
        const difference = targetDate - now;

        if (difference < 0) {
            countdownEl.innerHTML = "<span class='text-danger fw-bold font-subheading'>PROMOTION EXPIRED</span>";
            return;
        }

        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        const pad = (num) => num.toString().padStart(2, '0');
        const colors = ['cyan', 'cyan', 'cyan', 'pink'];
        const labels = ['Days', 'Hours', 'Mins', 'Secs'];
        const values = [days, hours, minutes, seconds];

        countdownEl.innerHTML = values.map((val, idx) => `
            <div class="d-inline-block text-center mx-2 my-1 p-3 glass-panel border-${colors[idx]} transition-smooth" style="min-width: 70px; animation: slideDown 0.5s cubic-bezier(0.4, 0, 0.2, 1) ${idx * 0.1}s both;">
                <span class="fs-3 fw-bold text-${colors[idx]} d-block">${pad(val)}</span>
                <small class="text-uppercase text-muted font-subheading" style="font-size: 0.75rem;">${labels[idx]}</small>
            </div>
        `).join('');
    };

    updateTimer();
    setInterval(updateTimer, 1000);
}

// Improved navbar highlight with smooth transitions
function highlightActiveNavbarLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active-page');
        }
    });
}

// Enhanced Scroll Reveal with stagger effect
function initScrollAnimations() {
    const revealElements = document.querySelectorAll('.reveal-on-scroll');
    if (revealElements.length === 0) return;

    const revealCallback = (entries, observer) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('active');
                }, index * 80);
                observer.unobserve(entry.target);
            }
        });
    };

    const revealObserver = new IntersectionObserver(revealCallback, {
        root: null,
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1), transform 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
        el.style.transitionDelay = `${index * 0.05}s`;
        revealObserver.observe(el);
    });

    // Add reveal-on-scroll active styles
    const style = document.createElement('style');
    style.innerHTML = `
        .reveal-on-scroll.active {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
}

// Enhanced button interactions with ripple effect
function initButtonInteractions() {
    const buttons = document.querySelectorAll('button, .btn, a.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mousedown', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                background: rgba(255, 255, 255, 0.5);
                border-radius: 50%;
                left: ${x}px;
                top: ${y}px;
                pointer-events: none;
                animation: ripple 0.6s ease-out;
            `;

            // Add ripple animation
            if (!this.style.position || this.style.position === 'static') {
                this.style.position = 'relative';
            }
            
            if (!document.querySelector('style[data-ripple-animation]')) {
                const style = document.createElement('style');
                style.setAttribute('data-ripple-animation', 'true');
                style.innerHTML = `
                    @keyframes ripple {
                        to {
                            transform: scale(4);
                            opacity: 0;
                        }
                    }
                `;
                document.head.appendChild(style);
            }

            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

// Enhanced form interactions
function initFormInteractions() {
    const formInputs = document.querySelectorAll('.form-glass, input, textarea, select');
    
    formInputs.forEach(input => {
        // Add smooth focus animation
        input.addEventListener('focus', function() {
            this.style.transform = 'translateY(-2px)';
        });

        input.addEventListener('blur', function() {
            this.style.transform = 'translateY(0)';
        });

        // Validate on blur
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('is-invalid');
            } else if (this.type === 'email' && this.value && !isValidEmail(this.value)) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });
}

// Email validation helper
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Accessibility features
function initAccessibilityFeatures() {
    // Improve focus management
    const interactiveElements = document.querySelectorAll('button, a, input, textarea, select, [role="button"]');
    
    interactiveElements.forEach(el => {
        el.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && (this.tagName === 'A' || this.hasAttribute('role') === 'button')) {
                this.click();
            }
        });
    });

    // Skip to main content link
    addSkipLink();

    // Add ARIA labels where needed
    const cartIcons = document.querySelectorAll('[id*="cart"]');
    cartIcons.forEach(icon => {
        if (!icon.hasAttribute('aria-label')) {
            icon.setAttribute('aria-label', 'Shopping cart');
        }
    });
}

// Add skip to main content link
function addSkipLink() {
    if (document.querySelector('.skip-to-main')) return;
    
    const skipLink = document.createElement('a');
    skipLink.className = 'skip-to-main';
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 0;
        background: var(--accent-blue);
        color: #000;
        padding: 8px;
        border-radius: 0 0 4px 0;
        z-index: 100;
        text-decoration: none;
        font-weight: bold;
    `;
    
    skipLink.addEventListener('focus', () => {
        skipLink.style.top = '0';
    });
    skipLink.addEventListener('blur', () => {
        skipLink.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
}

// Enhanced Quick Buy functionality
function initQuickBuyClickHandlers() {
    const buyBtns = document.querySelectorAll('.btn-quick-buy');
    buyBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const prodName = btn.dataset.productName || 'Product';
            
            // Neon alert overlay with enhanced styling
            const alertBox = document.createElement('div');
            alertBox.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: rgba(21, 21, 29, 0.95);
                border: 2px solid var(--accent-blue);
                box-shadow: 0 0 15px rgba(0, 229, 255, 0.4), 0 8px 24px rgba(0, 0, 0, 0.4);
                color: #fff;
                padding: 16px 24px;
                border-radius: 8px;
                backdrop-filter: blur(10px);
                z-index: 9999;
                font-family: 'Rajdhani', sans-serif;
                font-size: 1rem;
                font-weight: bold;
                letter-spacing: 1px;
                animation: slideDown 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
                box-sizing: border-box;
            `;
            
            alertBox.innerHTML = `
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="bi bi-cart-check-fill text-info" style="font-size: 1.3rem;"></i>
                    <span>${prodName.toUpperCase()} ADDED TO CART</span>
                </div>
            `;
            document.body.appendChild(alertBox);

            // Update cart badges with animation
            const cartBadges = document.querySelectorAll('.cart-badge');
            cartBadges.forEach(badge => {
                let currentVal = parseInt(badge.textContent || '0');
                badge.textContent = currentVal + 1;
                badge.style.animation = 'pulse 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
                setTimeout(() => {
                    badge.style.animation = '';
                }, 400);
            });

            // Slide out & cleanup with smooth animation
            setTimeout(() => {
                alertBox.style.animation = 'slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards';
                setTimeout(() => {
                    alertBox.remove();
                }, 400);
            }, 3000);
        });
    });
}

// Add pulse animation styles if not already present
if (!document.querySelector('style[data-pulse-animation]')) {
    const style = document.createElement('style');
    style.setAttribute('data-pulse-animation', 'true');
    style.innerHTML = `
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }
    `;
    document.head.appendChild(style);
}
