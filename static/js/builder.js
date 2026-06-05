/* Overclock PC Shop - Custom PC Builder Interactive Engine */

// Build state tracker
const BuildState = {
    cpu: null,
    mobo: null,
    gpu: null,
    ram: null,
    storage: null,
    psu: null,
    cooler: null,
    case: null
};

// Steps definition array
const STEPS = ['cpu', 'mobo', 'gpu', 'ram', 'storage', 'psu', 'cooler', 'case'];
let activeStepIndex = 0;

document.addEventListener('DOMContentLoaded', () => {
    // Only run if we are on the PC Builder page
    if (!document.getElementById('pc-builder-app')) return;

    // Load components
    initBuilderWizard();
});

function initBuilderWizard() {
    // 1. Set up step clicking logic
    const stepButtons = document.querySelectorAll('.builder-step-nav');
    stepButtons.forEach((btn, index) => {
        btn.addEventListener('click', () => {
            goToStep(index);
        });
    });

    // 2. Set up component selection logic
    const partCards = document.querySelectorAll('.part-select-card');
    partCards.forEach(card => {
        card.addEventListener('click', () => {
            selectPart(card);
        });
    });

    // 3. Set up Next/Prev buttons
    const prevBtn = document.getElementById('builder-prev-btn');
    const nextBtn = document.getElementById('builder-next-btn');

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (activeStepIndex > 0) goToStep(activeStepIndex - 1);
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            if (activeStepIndex < STEPS.length - 1) {
                goToStep(activeStepIndex + 1);
            } else {
                completeBuild();
            }
        });
    }

    // 4. Save build logic
    const saveBtn = document.getElementById('save-build-btn');
    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            saveBuildToProfile();
        });
    }

    // Initial render updates
    goToStep(0);
    updateStatsHUD();
}

function goToStep(index) {
    activeStepIndex = index;
    const currentStep = STEPS[activeStepIndex];

    // Update active nav state
    const stepNavs = document.querySelectorAll('.builder-step-nav');
    stepNavs.forEach((nav, idx) => {
        nav.classList.remove('active', 'border-info', 'text-info');
        if (idx === activeStepIndex) {
            nav.classList.add('active', 'border-info', 'text-info');
        } else if (idx < activeStepIndex) {
            nav.classList.add('text-success'); // step completed color
        }
    });

    // Toggle items display
    const partSections = document.querySelectorAll('.builder-parts-group');
    partSections.forEach(section => {
        section.classList.add('d-none');
        if (section.id === `parts-${currentStep}`) {
            section.classList.remove('d-none');
        }
    });

    // Update next/prev buttons labeling
    const prevBtn = document.getElementById('builder-prev-btn');
    const nextBtn = document.getElementById('builder-next-btn');

    if (prevBtn) {
        if (activeStepIndex === 0) {
            prevBtn.classList.add('disabled');
        } else {
            prevBtn.classList.remove('disabled');
        }
    }

    if (nextBtn) {
        if (activeStepIndex === STEPS.length - 1) {
            nextBtn.innerHTML = 'COMPLETE BUILD <i class="bi bi-patch-check-fill ms-2"></i>';
            nextBtn.classList.remove('btn-cyber');
            nextBtn.classList.add('btn', 'btn-outline-success', 'fw-bold');
        } else {
            nextBtn.innerHTML = 'NEXT STEP <i class="bi bi-chevron-right ms-1"></i>';
            nextBtn.classList.add('btn-cyber');
            nextBtn.classList.remove('btn', 'btn-outline-success', 'fw-bold');
        }
    }

    // Update instruction text
    const instructionEl = document.getElementById('builder-step-title');
    if (instructionEl) {
        instructionEl.textContent = `SELECT YOUR ${currentStep.toUpperCase()}`;
    }
}

function selectPart(card) {
    const step = card.dataset.stepType;
    const partId = card.dataset.partId;
    const partName = card.dataset.partName;
    const partPrice = parseFloat(card.dataset.partPrice);
    const partWattage = parseInt(card.dataset.partWattage || '0');
    const partSocket = card.dataset.partSocket || '';

    // Save configuration details
    BuildState[step] = {
        id: partId,
        name: partName,
        price: partPrice,
        wattage: partWattage,
        socket: partSocket
    };

    // Toggle UI card active class in current list
    const siblingCards = document.querySelectorAll(`.part-select-card[data-step-type="${step}"]`);
    siblingCards.forEach(c => c.classList.remove('active', 'border-info'));
    card.classList.add('active', 'border-info');

    // Update HUD summaries and check compatibility logs
    updateStatsHUD();
    checkCompatibility();
}

function checkCompatibility() {
    const logsEl = document.getElementById('compatibility-logs');
    if (!logsEl) return;

    logsEl.innerHTML = '';
    let warningsCount = 0;
    let successItems = [];

    // Socket compatibility check: CPU & Motherboard
    if (BuildState.cpu && BuildState.mobo) {
        if (BuildState.cpu.socket !== BuildState.mobo.socket) {
            warningsCount++;
            logsEl.innerHTML += `
                <div class="alert alert-danger py-2 px-3 mb-2" style="font-size: 0.9rem;">
                    <i class="bi bi-exclamation-triangle-fill text-danger me-2"></i>
                    <strong>SOCKET MISMATCH:</strong> CPU socket (${BuildState.cpu.socket}) is incompatible with Motherboard socket (${BuildState.mobo.socket}).
                </div>
            `;
        } else {
            successItems.push(`Socket compatibility checked: ${BuildState.cpu.socket} matched.`);
        }
    }

    // Wattage calculations: total vs PSU capacity
    const stats = calculateWattageAndCost();
    if (BuildState.psu) {
        const psuWatts = BuildState.psu.wattage;
        if (stats.wattage > psuWatts) {
            warningsCount++;
            logsEl.innerHTML += `
                <div class="alert alert-danger py-2 px-3 mb-2" style="font-size: 0.9rem;">
                    <i class="bi bi-lightning-fill text-danger me-2"></i>
                    <strong>POWER OVERLOAD:</strong> Total draw of ${stats.wattage}W exceeds your PSU capacity of ${psuWatts}W. Select a higher capacity power supply.
                </div>
            `;
        } else if (stats.wattage > psuWatts * 0.8) {
            logsEl.innerHTML += `
                <div class="alert alert-warning py-2 px-3 mb-2" style="font-size: 0.9rem;">
                    <i class="bi bi-exclamation-circle-fill text-warning me-2"></i>
                    <strong>HIGH LOAD ALERT:</strong> Power draw is at ${Math.round((stats.wattage/psuWatts)*100)}% of PSU rating. Recommend leaving 20% margin.
                </div>
            `;
        } else {
            successItems.push(`Power delivery load is safe: ${stats.wattage}W / ${psuWatts}W.`);
        }
    }

    // Render success configurations if no major issues
    if (warningsCount === 0) {
        logsEl.innerHTML += `
            <div class="alert alert-success py-2 px-3 mb-0" style="font-size: 0.9rem;">
                <i class="bi bi-shield-fill-check text-success me-2"></i>
                SYSTEM STATUS: All parts fully compatible. Optimized for peak gaming.
            </div>
        `;
    }

    // Update status badge
    const badgeEl = document.getElementById('compatibility-status-badge');
    if (badgeEl) {
        if (warningsCount > 0) {
            badgeEl.className = 'badge bg-danger text-light fw-bold px-2 py-1';
            badgeEl.innerHTML = '<i class="bi bi-x-circle-fill me-1"></i> ISSUES FOUND';
        } else {
            badgeEl.className = 'badge bg-success text-dark fw-bold px-2 py-1';
            badgeEl.innerHTML = '<i class="bi bi-check-circle-fill me-1"></i> COMPATIBLE';
        }
    }
}

function calculateWattageAndCost() {
    let cost = 0;
    let wattage = 0;

    for (let step of STEPS) {
        if (BuildState[step]) {
            cost += BuildState[step].price;
            // PSU does not draw power itself, it provides capacity, so exclude from sum calculation
            if (step !== 'psu') {
                wattage += BuildState[step].wattage;
            }
        }
    }

    return { cost, wattage };
}

function updateStatsHUD() {
    const stats = calculateWattageAndCost();

    // Update Price display
    const priceTextEls = document.querySelectorAll('.build-total-price');
    priceTextEls.forEach(el => {
        el.textContent = `$${stats.cost.toFixed(2)}`;
    });

    // Update Wattage text
    const wattTextEl = document.getElementById('build-total-wattage');
    if (wattTextEl) {
        wattTextEl.textContent = `${stats.wattage} W`;
    }

    // Update PSU capacity bar indicator
    const psuMax = BuildState.psu ? BuildState.psu.wattage : 850; // Default limit reference
    const barFillEl = document.getElementById('wattage-bar-fill');
    if (barFillEl) {
        const percent = Math.min((stats.wattage / psuMax) * 100, 100);
        barFillEl.style.width = `${percent}%`;
        
        // Colors warning shifts
        if (percent > 90) {
            barFillEl.className = 'wattage-fill bg-danger';
        } else if (percent > 75) {
            barFillEl.className = 'wattage-fill bg-warning';
        } else {
            barFillEl.className = 'wattage-fill bg-info';
        }
    }

    // Update summary table in UI sidebar
    for (let step of STEPS) {
        const nameEl = document.getElementById(`summary-${step}-name`);
        const priceEl = document.getElementById(`summary-${step}-price`);
        const rowEl = document.getElementById(`summary-${step}-row`);

        if (BuildState[step]) {
            if (nameEl) nameEl.textContent = BuildState[step].name;
            if (priceEl) priceEl.textContent = `$${BuildState[step].price.toFixed(2)}`;
            if (rowEl) rowEl.classList.remove('opacity-50');
        } else {
            if (nameEl) nameEl.textContent = 'Not Selected';
            if (priceEl) priceEl.textContent = '-';
            if (rowEl) rowEl.classList.add('opacity-50');
        }
    }

    // Update progress percentage
    let selectedCount = 0;
    for (let step of STEPS) {
        if (BuildState[step]) selectedCount++;
    }
    const progressPercent = Math.round((selectedCount / STEPS.length) * 100);
    const progressEl = document.getElementById('build-progress-percent');
    const progressBarEl = document.getElementById('build-progress-bar');

    if (progressEl) progressEl.textContent = `${progressPercent}%`;
    if (progressBarEl) progressBarEl.style.width = `${progressPercent}%`;
}

function completeBuild() {
    // Make sure we have selected everything before redirecting or loading
    let missingSteps = [];
    for (let step of STEPS) {
        if (!BuildState[step]) {
            missingSteps.push(step.toUpperCase());
        }
    }

    if (missingSteps.length > 0) {
        alert(`Your custom build is incomplete. Please select components for: ${missingSteps.join(', ')}.`);
        // Find first incomplete step and navigate
        const firstMissing = STEPS.findIndex(step => !BuildState[step]);
        goToStep(firstMissing);
        return;
    }

    // Custom success confirmation overlay
    const modalHtml = `
        <div class="modal fade" id="buildCompleteModal" tabindex="-1" aria-hidden="true" style="backdrop-filter: blur(10px);">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content glass-panel border-cyan" style="background: var(--bg-secondary); color: #fff;">
                    <div class="modal-header border-0 pb-0">
                        <h5 class="modal-title font-heading text-info">Custom System Assembled</h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body text-center py-4">
                        <div class="success-checkmark mb-3">
                            <i class="bi bi-cpu text-info"></i>
                        </div>
                        <h4 class="font-heading mb-2">Build Completed!</h4>
                        <p class="text-gray mb-4">Your personalized battlestation configuration is locked in and ready for shipping.</p>
                        <div class="p-3 glass-panel mb-4 bg-dark">
                            <div class="d-flex justify-content-between mb-2">
                                <span class="text-muted">Total Power Draw:</span>
                                <span class="fw-bold text-info">${calculateWattageAndCost().wattage} Watts</span>
                            </div>
                            <div class="d-flex justify-content-between">
                                <span class="text-muted">Total Est Price:</span>
                                <span class="fw-bold text-pink">$${calculateWattageAndCost().cost.toFixed(2)}</span>
                            </div>
                        </div>
                        <div class="d-grid gap-2">
                            <button type="button" id="modal-add-to-cart-btn" class="btn btn-cyber fw-bold text-uppercase">ADD ASSEMBLED RIG TO CART</button>
                            <button type="button" class="btn text-muted btn-link text-decoration-none" data-bs-dismiss="modal">Modify Specs</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Append to body and show
    const wrapper = document.createElement('div');
    wrapper.innerHTML = modalHtml;
    document.body.appendChild(wrapper);

    const modalObj = new bootstrap.Modal(document.getElementById('buildCompleteModal'));
    modalObj.show();

    document.getElementById('modal-add-to-cart-btn').addEventListener('click', () => {
        modalObj.hide();
        // Redirect to cart
        window.location.href = '/cart/';
    });
}

function saveBuildToProfile() {
    let selectedCount = 0;
    for (let step of STEPS) {
        if (BuildState[step]) selectedCount++;
    }

    if (selectedCount === 0) {
        alert('Please choose some hardware components before saving.');
        return;
    }

    const stats = calculateWattageAndCost();
    const buildName = prompt('Enter a custom name for your setup:', 'Project CyberRig');
    if (!buildName) return;

    // Save details in local storage for access in user profile
    const savedBuildObj = {
        name: buildName,
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        price: stats.cost,
        wattage: stats.wattage,
        specs: `${BuildState.cpu?.name || 'No CPU'} | ${BuildState.gpu?.name || 'No GPU'} | ${BuildState.ram?.name || 'No RAM'}`
    };

    let existingBuilds = JSON.parse(localStorage.getItem('saved_custom_builds') || '[]');
    existingBuilds.unshift(savedBuildObj);
    localStorage.setItem('saved_custom_builds', JSON.stringify(existingBuilds));

    alert(`Rig "${buildName}" has been successfully saved to your neural terminal saved builds bank.`);
}
