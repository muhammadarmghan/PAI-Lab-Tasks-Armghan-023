/*
 * Weather App - Frontend JavaScript
 * Handles API communication and dynamic UI updates
 */

// Backend API URL
const API_URL = 'http://localhost:5000';

// Get DOM elements
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const weatherResult = document.getElementById('weatherResult');
const errorDiv = document.getElementById('error');
const loadingDiv = document.getElementById('loading');

// Event listeners
searchBtn.addEventListener('click', searchWeather);
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchWeather();
    }
});

/**
 * Search for weather of a city
 */
function searchWeather() {
    const cityName = cityInput.value.trim();
    
    // Validate input
    if (!cityName) {
        showError('Please enter a city name', 'Empty Input');
        return;
    }
    
    if (cityName.length < 2) {
        showError('City name must be at least 2 characters', 'Invalid Input');
        return;
    }
    
    // Hide previous results
    hideAll();
    
    // Show loading
    loadingDiv.style.display = 'block';
    
    // Fetch weather data
    fetch(`${API_URL}/weather?city=${encodeURIComponent(cityName)}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Unknown error occurred');
                });
            }
            return response.json();
        })
        .then(data => {
            loadingDiv.style.display = 'none';
            displayWeather(data);
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            console.error('Error:', error);
            showError(
                error.message || 'Could not fetch weather data. Please try again.',
                'Network Error'
            );
        });
}

/**
 * Display weather data on the page
 * @param {Object} data - Weather data from API
 */
function displayWeather(data) {
    // Update DOM elements with weather data
    document.getElementById('cityName').textContent = data.city;
    document.getElementById('condition').textContent = data.condition;
    document.getElementById('weatherEmoji').textContent = data.emoji;
    document.getElementById('temperature').textContent = `${data.temperature}${data.unit_temp}`;
    document.getElementById('humidity').textContent = `${data.humidity}%`;
    document.getElementById('windSpeed').textContent = `${data.wind_speed} ${data.unit_wind}`;
    
    // Show results
    weatherResult.style.display = 'block';
    
    // Scroll to results
    weatherResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Clear input for next search
    cityInput.value = '';
    cityInput.focus();
}

/**
 * Show error message
 * @param {string} message - Error message
 * @param {string} title - Error title
 */
function showError(message, title = 'Error') {
    document.getElementById('errorTitle').textContent = title;
    document.getElementById('errorText').textContent = message;
    errorDiv.style.display = 'block';
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        if (errorDiv.style.display !== 'none') {
            errorDiv.style.display = 'none';
        }
    }, 5000);
}

/**
 * Hide all result containers
 */
function hideAll() {
    weatherResult.style.display = 'none';
    errorDiv.style.display = 'none';
    loadingDiv.style.display = 'none';
}
