// DOM Elements
const queryInput = document.getElementById('queryInput');
const searchBtn = document.getElementById('searchBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsContainer = document.getElementById('resultsContainer');

// Event Listeners
searchBtn.addEventListener('click', performSearch);
queryInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

// Perform Search
async function performSearch() {
    const query = queryInput.value.trim();

    if (!query) {
        alert('Please enter a query');
        return;
    }

    // Show loading spinner
    loadingSpinner.classList.remove('hidden');
    resultsContainer.innerHTML = '';

    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query: query,
                top_k: 3
            })
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data.results, data.query);
        } else {
            showError(data.error || 'An error occurred');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to connect to the server');
    } finally {
        // Hide loading spinner
        loadingSpinner.classList.add('hidden');
    }
}

// Display Results
function displayResults(results, query) {
    if (results.length === 0) {
        resultsContainer.innerHTML = `
            <div class="no-results">
                <h3>No results found</h3>
                <p>Try a different query or check the examples below.</p>
            </div>
        `;
        return;
    }

    resultsContainer.innerHTML = results.map(result => `
        <div class="result-item">
            <div class="result-rank">#${result.rank}</div>
            <div class="result-question">❓ ${escapeHtml(result.question)}</div>
            <div class="result-answer">${escapeHtml(result.answer)}</div>
            <span class="result-similarity">Match: ${(result.similarity * 100).toFixed(1)}%</span>
        </div>
    `).join('');
}

// Show Error
function showError(message) {
    resultsContainer.innerHTML = `
        <div class="no-results">
            <h3>❌ Error</h3>
            <p>${escapeHtml(message)}</p>
        </div>
    `;
}

// Helper: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Focus input on load
window.addEventListener('load', () => {
    queryInput.focus();
});
