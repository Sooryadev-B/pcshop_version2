/* Overclock PC Shop - Admin Dashboard Charts Controller */

document.addEventListener('DOMContentLoaded', () => {
    // Only execute on admin panel view
    if (!document.getElementById('admin-dashboard-view')) return;

    initAdminCharts();
    initRestockButtons();
});

function initAdminCharts() {
    // Chart.js global style settings for dark mode
    Chart.defaults.color = '#9ca3af';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.05)';
    Chart.defaults.font.family = "'Rajdhani', sans-serif";
    Chart.defaults.font.size = 13;

    // 1. Sales Trend Chart
    const salesCtx = document.getElementById('salesTrendChart');
    if (salesCtx) {
        new Chart(salesCtx, {
            type: 'line',
            data: {
                labels: ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May'],
                datasets: [{
                    label: 'Gross Sales ($)',
                    data: [42000, 58000, 49000, 78000, 92000, 142589.90],
                    borderColor: '#00e5ff',
                    backgroundColor: 'rgba(0, 229, 255, 0.05)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#8b5cf6',
                    pointBorderColor: '#fff',
                    pointHoverRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: '#15151d',
                        borderColor: '#00e5ff',
                        borderWidth: 1,
                        titleFont: { size: 14, weight: 'bold' },
                        bodyFont: { size: 14 },
                        padding: 10
                    }
                },
                scales: {
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    // 2. Product Category Doughnut Chart
    const categoryCtx = document.getElementById('categoryShareChart');
    if (categoryCtx) {
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: ['Prebuilt Rigs', 'GPUs', 'CPUs', 'RAM', 'Storage'],
                datasets: [{
                    data: [55, 20, 12, 8, 5],
                    backgroundColor: [
                        '#8b5cf6', // purple
                        '#00e5ff', // blue
                        '#ff00ff', // pink
                        '#3b82f6', // indigo
                        '#10b981'  // emerald
                    ],
                    borderWidth: 1,
                    borderColor: '#15151d'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 12,
                            padding: 15
                        }
                    },
                    tooltip: {
                        backgroundColor: '#15151d',
                        borderColor: '#8b5cf6',
                        borderWidth: 1,
                        padding: 10
                    }
                },
                cutout: '70%'
            }
        });
    }
}

function initRestockButtons() {
    const restockBtns = document.querySelectorAll('.btn-restock');
    restockBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const row = btn.closest('tr');
            const itemName = row.querySelector('.stock-item-name')?.textContent || 'Item';
            const quantityInput = prompt(`Enter restock volume units for "${itemName.trim()}":`, '10');
            
            if (quantityInput === null) return;
            const quantity = parseInt(quantityInput);
            if (isNaN(quantity) || quantity <= 0) {
                alert('Invalid restock volume format.');
                return;
            }

            // Update UI values
            const stockValEl = row.querySelector('.stock-val');
            if (stockValEl) {
                let currentStock = parseInt(stockValEl.textContent || '0');
                let newStock = currentStock + quantity;
                stockValEl.textContent = newStock;
                
                // Update badge if stock becomes sufficient
                const badgeEl = row.querySelector('.stock-badge-container span');
                if (badgeEl && newStock >= 10) {
                    badgeEl.className = 'badge bg-success text-dark';
                    badgeEl.textContent = 'In Stock';
                }
            }

            alert(`Secured restock batch: +${quantity} units added for ${itemName.trim()}.`);
        });
    });
}
