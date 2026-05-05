"""
Weather App - Flask Backend
Complete implementation with:
- Flask app with CORS enabled
- Weather API integration (Open-Meteo)
- Proper error handling
- Dashboard with statistics
- Request logging and monitoring
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import logging
from datetime import datetime, timedelta
from collections import defaultdict

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Statistics tracking
stats = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'total_cities_searched': set(),
    'request_history': [],
    'api_calls': 0,
    'start_time': datetime.now()
}

# Weather API endpoint (Open-Meteo - no API key needed)
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_API = "https://api.open-meteo.com/v1/forecast"

# Weather condition mapping
WEATHER_CONDITIONS = {
    0: "Clear",
    1: "Clear",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Foggy",
    48: "Foggy",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    80: "Light Showers",
    81: "Showers",
    82: "Heavy Showers",
    85: "Light Snow Showers",
    86: "Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Hail",
    99: "Thunderstorm with Hail",
}

# Weather emoji mapping
WEATHER_EMOJI = {
    "Clear": "☀️",
    "Cloudy": "☁️",
    "Partly Cloudy": "⛅",
    "Foggy": "🌫️",
    "Drizzle": "🌦️",
    "Rain": "🌧️",
    "Snow": "❄️",
    "Thunderstorm": "⛈️",
}


def log_request(city, status, temperature=None, condition=None, error=None):
    """Log request to statistics"""
    stats['total_requests'] += 1
    
    if status == 'success':
        stats['successful_requests'] += 1
        stats['total_cities_searched'].add(city)
    else:
        stats['failed_requests'] += 1
    
    request_log = {
        'timestamp': datetime.now().isoformat(),
        'city': city,
        'status': status,
        'temperature': temperature,
        'condition': condition,
        'error': error
    }
    
    stats['request_history'].append(request_log)
    
    # Keep only last 100 requests
    if len(stats['request_history']) > 100:
        stats['request_history'] = stats['request_history'][-100:]


@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Get weather data for a city
    Query parameters:
        - city (string): City name to get weather for
    Returns:
        JSON with: city, temperature, condition, humidity, wind_speed
    """
    try:
        # Get city name from query parameter
        city_name = request.args.get('city', '').strip()
        
        # Validate input
        if not city_name:
            return jsonify({
                'error': 'City name is required',
                'message': 'Please provide a city name as a query parameter'
            }), 400
        
        if len(city_name) < 2:
            return jsonify({
                'error': 'Invalid city name',
                'message': 'City name must be at least 2 characters'
            }), 400
        
        logger.info(f"Fetching weather for: {city_name}")
        
        # Step 1: Get coordinates of the city
        geo_params = {
            'name': city_name,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        
        geo_response = requests.get(GEOCODING_API, params=geo_params, timeout=5)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        # Check if city was found
        if not geo_data.get('results'):
            log_request(city_name, 'error', error='City not found')
            return jsonify({
                'error': 'City not found',
                'message': f'Could not find city: {city_name}'
            }), 404
        
        # Get the first result
        location = geo_data['results'][0]
        latitude = location['latitude']
        longitude = location['longitude']
        actual_city_name = location['name']
        country = location.get('country', '')
        
        logger.info(f"Found city: {actual_city_name}, {country} ({latitude}, {longitude})")
        
        # Step 2: Get weather data for the coordinates
        weather_params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m',
            'timezone': 'auto'
        }
        
        weather_response = requests.get(WEATHER_API, params=weather_params, timeout=5)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Extract current weather
        current = weather_data['current']
        temperature = current['temperature_2m']
        humidity = current['relative_humidity_2m']
        wind_speed = current['wind_speed_10m']
        weather_code = current['weather_code']
        
        # Get weather condition from code
        condition = WEATHER_CONDITIONS.get(weather_code, 'Unknown')
        emoji = WEATHER_EMOJI.get(condition, '🌤️')
        
        # Prepare response
        response = {
            'city': f"{actual_city_name}, {country}",
            'temperature': temperature,
            'condition': condition,
            'emoji': emoji,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'unit_temp': '°C',
            'unit_wind': 'km/h'
        }
        
        # Log successful request
        log_request(city_name, 'success', temperature, condition)
        stats['api_calls'] += 1
        logger.info(f"Successfully fetched weather: {response}")
        return jsonify(response), 200
    
    except requests.exceptions.Timeout:
        log_request(city_name, 'error', error='API timeout')
        logger.error("API request timed out")
        return jsonify({
            'error': 'Request timeout',
            'message': 'Weather API is not responding. Please try again.'
        }), 503
    
    except requests.exceptions.ConnectionError:
        log_request(city_name, 'error', error='Connection error')
        logger.error("Connection error")
        return jsonify({
            'error': 'Connection error',
            'message': 'Could not connect to weather service. Check your internet connection.'
        }), 503
    
    except requests.exceptions.RequestException as e:
        log_request(city_name, 'error', error=str(e))
        logger.error(f"API error: {str(e)}")
        return jsonify({
            'error': 'API error',
            'message': 'Error fetching weather data. Please try again.'
        }), 500
    
    except Exception as e:
        log_request(city_name, 'error', error=str(e))
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred.'
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Weather API is running'}), 200


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Admin dashboard with statistics and monitoring"""
    uptime = datetime.now() - stats['start_time']
    uptime_str = str(uptime).split('.')[0]
    
    success_rate = 0
    if stats['total_requests'] > 0:
        success_rate = (stats['successful_requests'] / stats['total_requests']) * 100
    
    dashboard_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather API - Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { max-width: 1400px; margin: 0 auto; }
            .header {
                background: rgba(255,255,255,0.95);
                padding: 30px;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            }
            .header h1 { color: #667eea; margin-bottom: 10px; }
            .header p { color: #666; }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border-left: 5px solid #667eea;
            }
            .stat-label { color: #999; font-size: 0.9em; margin-bottom: 10px; }
            .stat-value { font-size: 2.5em; font-weight: bold; color: #333; }
            .stat-unit { color: #999; font-size: 0.6em; margin-left: 10px; }
            .request-history {
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .request-history h2 { color: #667eea; margin-bottom: 20px; }
            .request-item {
                padding: 12px;
                border-bottom: 1px solid #eee;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .request-item:last-child { border-bottom: none; }
            .status-badge {
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85em;
                font-weight: bold;
            }
            .status-success { background: #d4edda; color: #155724; }
            .status-error { background: #f8d7da; color: #721c24; }
            .time { color: #999; font-size: 0.9em; }
            .refresh-btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin-top: 20px;
            }
            .refresh-btn:hover { background: #764ba2; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Weather API Dashboard</h1>
                <p>Real-time monitoring and statistics</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Requests</div>
                    <div class="stat-value">""" + str(stats['total_requests']) + """</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Successful</div>
                    <div class="stat-value" style="color: #4CAF50;">""" + str(stats['successful_requests']) + """</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Failed</div>
                    <div class="stat-value" style="color: #F44336;">""" + str(stats['failed_requests']) + """</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Success Rate</div>
                    <div class="stat-value" style="color: #2196F3;">""" + f"{success_rate:.1f}" + """<span class="stat-unit">%</span></div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Unique Cities</div>
                    <div class="stat-value">""" + str(len(stats['total_cities_searched'])) + """</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">API Uptime</div>
                    <div class="stat-value" style="font-size: 1.5em;">""" + uptime_str + """</div>
                </div>
            </div>
            
            <div class="request-history">
                <h2>📋 Recent Requests (Last 20)</h2>
                """ + "".join([f"""
                <div class="request-item">
                    <div>
                        <strong>{req['city']}</strong><br>
                        <span class="time">{req['timestamp']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span class="status-badge status-{'success' if req['status'] == 'success' else 'error'}">
                            {req['status'].upper()}
                        </span>
                        {f"<div style='color: #666; font-size: 0.9em; margin-top: 5px;'>{req['condition']} {req['temperature']}°C</div>" if req['condition'] else ""}
                    </div>
                </div>
                """ for req in reversed(stats['request_history'][-20:])]) + """
                <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button>
            </div>
        </div>
    </body>
    </html>
    """
    return dashboard_html


@app.route('/', methods=['GET'])
def index():
    """Welcome page with API documentation and explorer"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather API - Flask Backend</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }
            .content {
                padding: 40px;
            }
            .section {
                margin-bottom: 40px;
            }
            .section h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.5em;
            }
            .api-test {
                background: #f5f5f5;
                padding: 20px;
                border-radius: 8px;
                margin-top: 20px;
            }
            .test-input {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }
            input {
                flex: 1;
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 1em;
            }
            button {
                padding: 12px 30px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s;
            }
            button:hover {
                background: #764ba2;
                transform: translateY(-2px);
            }
            .response {
                background: #1e1e1e;
                color: #00ff00;
                padding: 20px;
                border-radius: 5px;
                margin-top: 15px;
                font-family: 'Courier New', monospace;
                max-height: 400px;
                overflow-y: auto;
                display: none;
            }
            .response.show {
                display: block;
            }
            .endpoint {
                background: #f9f9f9;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            }
            .method {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 0.9em;
                margin-right: 10px;
            }
            .method.get {
                background: #4CAF50;
                color: white;
            }
            .status {
                margin-top: 15px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .status.show {
                display: block;
            }
            .status.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .status.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .footer {
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #666;
                border-top: 1px solid #ddd;
            }
            .link {
                color: #667eea;
                text-decoration: none;
                font-weight: bold;
            }
            .link:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌤️ Weather API</h1>
                <p>Flask Backend - Real-time Weather Data</p>
            </div>
            
            <div class="content">
                <!-- API Documentation -->
                <div class="section">
                    <h2>📚 API Endpoints</h2>
                    
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <strong>/weather</strong>
                        <p style="margin-top: 10px; color: #666;">Get weather for a city</p>
                        <p><strong>Parameters:</strong> city (required)</p>
                        <p><strong>Example:</strong> /weather?city=London</p>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <strong>/health</strong>
                        <p style="margin-top: 10px; color: #666;">Check API status</p>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <strong>/dashboard</strong>
                        <p style="margin-top: 10px; color: #666;">Admin dashboard with statistics and monitoring</p>
                    </div>
                    
                    <div class="endpoint">
                        <span class="method get">GET</span>
                        <strong>/</strong>
                        <p style="margin-top: 10px; color: #666;">API documentation (this page)</p>
                    </div>
                </div>
                
                <!-- API Tester -->
                <div class="section">
                    <h2>🧪 Test API</h2>
                    <div class="api-test">
                        <div class="test-input">
                            <input 
                                type="text" 
                                id="cityInput" 
                                placeholder="Enter city name (e.g., London, Paris, Tokyo)"
                                autocomplete="off"
                            >
                            <button onclick="testWeatherAPI()">Get Weather</button>
                        </div>
                        <div id="status" class="status"></div>
                        <div id="response" class="response"></div>
                    </div>
                </div>
                
                <!-- Info -->
                <div class="section">
                    <h2>ℹ️ Information</h2>
                    <p><strong>Frontend:</strong> <a href="http://localhost:8000" class="link">http://localhost:8000</a></p>
                    <p><strong>Backend:</strong> <a href="http://localhost:5000" class="link">http://localhost:5000</a></p>
                    <p><strong>Dashboard:</strong> <a href="http://localhost:5000/dashboard" class="link">http://localhost:5000/dashboard</a></p>
                    <p><strong>Data Source:</strong> Open-Meteo API (Free, No Authentication)</p>
                </div>
            </div>
            
            <div class="footer">
                <p>🚀 Weather App - Flask Backend | Made with ❤️</p>
            </div>
        </div>
        
        <script>
            async function testWeatherAPI() {
                const city = document.getElementById('cityInput').value.trim();
                const statusDiv = document.getElementById('status');
                const responseDiv = document.getElementById('response');
                
                if (!city) {
                    statusDiv.textContent = 'Please enter a city name';
                    statusDiv.className = 'status show error';
                    responseDiv.className = 'response';
                    return;
                }
                
                try {
                    statusDiv.textContent = 'Loading...';
                    statusDiv.className = 'status show';
                    
                    const response = await fetch(`/weather?city=${encodeURIComponent(city)}`);
                    const data = await response.json();
                    
                    responseDiv.textContent = JSON.stringify(data, null, 2);
                    responseDiv.className = 'response show';
                    
                    if (response.ok) {
                        statusDiv.textContent = '✅ Success! Weather data fetched successfully.';
                        statusDiv.className = 'status show success';
                    } else {
                        statusDiv.textContent = '❌ Error: ' + (data.message || 'Unknown error');
                        statusDiv.className = 'status show error';
                    }
                } catch (error) {
                    statusDiv.textContent = '❌ Error: ' + error.message;
                    statusDiv.className = 'status show error';
                    responseDiv.className = 'response';
                }
            }
            
            // Allow Enter key
            document.getElementById('cityInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') testWeatherAPI();
            });
        </script>
    </body>
    </html>
    """
    return html


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The HTTP method is not allowed for this endpoint'
    }), 405


if __name__ == '__main__':
    logger.info("Starting Weather API Flask Server...")
    logger.info("Server running at http://localhost:5000")
    logger.info("Press CTRL+C to stop the server")
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
