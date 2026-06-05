/* Overclock PC Shop - Shopping Cart Interactivity */

document.addEventListener('DOMContentLoaded', () => {
    // Check if we are on the Shopping Cart or Checkout page
    if (document.getElementById('cart-page-container')) {
        initCartPage();
    }
});

function initCartPage() {
    // 1. Quantity Adjuster hooks
    const minusBtns = document.querySelectorAll('.qty-minus');
    const plusBtns = document.querySelectorAll('.qty-plus');

    minusBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            adjustQuantity(btn, -1);
        });
    });

    plusBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            adjustQuantity(btn, 1);
        });
    });

    // 2. Remove item buttons
    const removeBtns = document.querySelectorAll('.cart-remove-item');
    removeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            removeItem(btn);
        });
    });

    // 3. Coupon form submission
    const couponForm = document.getElementById('coupon-apply-form');
    if (couponForm) {
        couponForm.addEventListener('submit', (e) => {
            e.preventDefault();
            applyCoupon();
        });
    }

    // 4. Shipping Calculator
    const shipBtn = document.getElementById('calc-shipping-btn');
    if (shipBtn) {
        shipBtn.addEventListener('click', () => {
            calculateShippingTime();
        });
    }

    // Initialize values
    recalculateCartTotals();
}

function adjustQuantity(button, change) {
    const itemRow = button.closest('.cart-item-row');
    const qtyInput = itemRow.querySelector('.cart-qty-input');
    let currentVal = parseInt(qtyInput.value || '1');
    
    currentVal = Math.max(1, currentVal + change);
    qtyInput.value = currentVal;

    // Update item total price display
    const itemPrice = parseFloat(qtyInput.dataset.itemUnitPrice);
    const totalEl = itemRow.querySelector('.cart-item-total');
    if (totalEl) {
        totalEl.textContent = `$${(itemPrice * currentVal).toFixed(2)}`;
    }

    recalculateCartTotals();
}

function removeItem(button) {
    const itemRow = button.closest('.cart-item-row');
    const name = itemRow.querySelector('.cart-item-name')?.textContent || 'Hardware Item';
    
    if (confirm(`Remove "${name.trim()}" from neural cart repository?`)) {
        itemRow.classList.add('fade-out');
        setTimeout(() => {
            itemRow.remove();
            
            // If cart is empty, show empty state
            const remainingRows = document.querySelectorAll('.cart-item-row');
            if (remainingRows.length === 0) {
                const cartContainer = document.getElementById('cart-page-container');
                cartContainer.innerHTML = `
                    <div class="text-center py-5 glass-panel border-cyan">
                        <i class="bi bi-cart-x fs-1 text-muted d-block mb-3"></i>
                        <h3 class="font-heading">YOUR TERMINAL CART IS EMPTY</h3>
                        <p class="text-gray mb-4">No high-performance hardware configurations found.</p>
                        <a href="/catalog/" class="btn btn-cyber font-subheading">GO BACK TO SHOPPING</a>
                    </div>
                `;
            }
            
            recalculateCartTotals();
        }, 300);
    }
}

// Variables for discounts
let currentDiscountRate = 0;
let appliedPromoCode = "";

function applyCoupon() {
    const couponInput = document.getElementById('coupon-code-input');
    const messageEl = document.getElementById('coupon-status-message');
    if (!couponInput || !messageEl) return;

    const code = couponInput.value.trim().toUpperCase();

    if (code === 'OVERCLOCK15') {
        currentDiscountRate = 0.15;
        appliedPromoCode = "OVERCLOCK15";
        messageEl.className = 'text-success mt-2 font-subheading';
        messageEl.innerHTML = `<i class="bi bi-patch-check-fill me-1"></i> Promo code OVERCLOCK15 applied: 15% discount activated!`;
        couponInput.setAttribute('disabled', 'true');
        document.getElementById('coupon-apply-btn').setAttribute('disabled', 'true');
    } else if (code === '') {
        messageEl.className = 'text-warning mt-2 font-subheading';
        messageEl.innerHTML = `Please enter a valid neural decrypt code.`;
    } else {
        messageEl.className = 'text-danger mt-2 font-subheading';
        messageEl.innerHTML = `<i class="bi bi-exclamation-triangle-fill me-1"></i> Decrypt failed: Invalid promo code.`;
    }

    recalculateCartTotals();
}

function calculateShippingTime() {
    const zipInput = document.getElementById('shipping-zip-input');
    const statusEl = document.getElementById('shipping-calc-status');
    if (!zipInput || !statusEl) return;

    const zipVal = zipInput.value.trim();
    if (zipVal.length < 3) {
        statusEl.className = 'text-danger mt-2 font-subheading';
        statusEl.innerHTML = 'Enter a valid routing zip address.';
        return;
    }

    statusEl.className = 'text-info mt-2 font-subheading';
    statusEl.innerHTML = `
        <div class="d-flex align-items-center mt-2">
            <div class="spinner-border spinner-border-sm text-info me-2" role="status"></div>
            <span>Scanning shipping channels...</span>
        </div>
    `;

    setTimeout(() => {
        const days = Math.floor(Math.random() * 3) + 2;
        statusEl.className = 'text-success mt-2 font-subheading';
        statusEl.innerHTML = `<i class="bi bi-cursor-fill me-1"></i> Hyper-Drone delivery to ZIP ${zipVal} available: Estimated ${days} days.`;
    }, 1200);
}

function recalculateCartTotals() {
    const itemRows = document.querySelectorAll('.cart-item-row');
    let subtotal = 0;

    itemRows.forEach(row => {
        const qtyInput = row.querySelector('.cart-qty-input');
        if (qtyInput) {
            const qty = parseInt(qtyInput.value || '1');
            const unitPrice = parseFloat(qtyInput.dataset.itemUnitPrice);
            subtotal += qty * unitPrice;
        }
    });

    // Upgrades pricing if detail configuration is on the row
    // Let's check for custom elements
    const upgradeOptions = document.querySelectorAll('.cart-item-upgrade-cost');
    upgradeOptions.forEach(el => {
        subtotal += parseFloat(el.dataset.upgradePrice || '0');
    });

    // Update Subtotal element
    const subtotalEl = document.getElementById('cart-summary-subtotal');
    if (subtotalEl) {
        subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
    }

    // Update Discount elements
    let discountVal = subtotal * currentDiscountRate;
    const discountEl = document.getElementById('cart-summary-discount');
    const discountRow = document.getElementById('cart-summary-discount-row');
    if (discountEl && discountRow) {
        if (discountVal > 0) {
            discountEl.textContent = `-$${discountVal.toFixed(2)}`;
            discountRow.classList.remove('d-none');
        } else {
            discountRow.classList.add('d-none');
        }
    }

    // Shipping rules: Free shipping for orders above $4,000, otherwise $49.99
    let shipping = subtotal > 4000 ? 0.00 : 49.99;
    const shippingEl = document.getElementById('cart-summary-shipping');
    if (shippingEl) {
        shippingEl.textContent = shipping === 0 ? 'FREE' : `$${shipping.toFixed(2)}`;
        if (shipping === 0) {
            shippingEl.className = 'text-success fw-bold';
        } else {
            shippingEl.className = 'text-white';
        }
    }

    // Update Final Total
    const total = subtotal - discountVal + shipping;
    const totalEl = document.getElementById('cart-summary-total');
    if (totalEl) {
        totalEl.textContent = `$${total.toFixed(2)}`;
    }
}
