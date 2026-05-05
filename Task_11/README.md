# Task 1: Weather App (Flask + Dynamic Frontend)

## Project Overview
Build a **Weather Application** with:
- **Backend**: Flask (Python)
- **Frontend**: HTML/CSS/JavaScript (Dynamic)
- **API**: Free weather API (OpenWeatherMap, WeatherAPI, or similar)

---

## Project Structure
```
Task_1_Weather_App/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # API keys (DO NOT COMMIT)
├── frontend/
│   ├── index.html             # Main page
│   ├── style.css              # Styling
│   └── script.js              # Dynamic functionality
└── README.md                   # This file
```

---

## Step-by-Step Instructions

### **Step 1: Choose a Free Weather API**
Pick one and sign up for a free API key:
- **OpenWeatherMap** (https://openweathermap.org/api) - Good for current weather
- **WeatherAPI** (https://www.weatherapi.com) - Includes forecasts
- **Open-Meteo** (https://open-meteo.com) - No API key needed!

**Recommendation**: Use Open-Meteo (no authentication required) or OpenWeatherMap free tier

---

### **Step 2: Set Up Backend (Flask)**

#### 2.1 Create Virtual Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
```

#### 2.2 Create `requirements.txt`
```
Flask==2.3.0
Flask-CORS==4.0.0
requests==2.31.0
python-dotenv==1.0.0
```

#### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2.4 Create `app.py` with Flask Routes

**What your backend should do:**
1. Create a Flask app with CORS enabled (so frontend can call it)
2. Create a `/weather` endpoint that:
   - Accepts a city name as parameter
   - Calls the weather API
   - Returns JSON with: temperature, condition, humidity, wind speed, city name
3. Handle errors gracefully (city not found, API errors)

**Example endpoint structure:**
```
GET /weather?city=London
Returns: {
    "city": "London",
    "temperature": 15,
    "condition": "Cloudy",
    "humidity": 72,
    "wind_speed": 8
}
```

#### 2.5 Create `.env` file (if using API that needs key)
```
WEATHER_API_KEY=your_api_key_here
```

---

### **Step 3: Set Up Frontend (Dynamic)**

#### 3.1 Create `index.html`
**Requirements:**
- Search input field for city name
- Submit button
- Display area for weather information
- Show: Temperature, condition, humidity, wind speed, city name
- Add an icon/image based on weather condition

#### 3.2 Create `style.css`
- Make it visually appealing
- Responsive design (mobile-friendly)
- Good color scheme (blue for sky, sun colors, etc.)
- Smooth animations/transitions

#### 3.3 Create `script.js` (Dynamic Functionality)
**What it should do:**
1. Get the city name from input field
2. Make a fetch request to `http://localhost:5000/weather?city={city}`
3. Display results dynamically (no page reload)
4. Show loading state while fetching
5. Show error messages if something fails
6. Clear previous results when searching again

**Example fetch structure:**
```javascript
fetch(`http://localhost:5000/weather?city=${cityName}`)
    .then(response => response.json())
    .then(data => displayWeather(data))
    .catch(error => showError(error));
```

---

## Implementation Checklist

### Backend
- [ ] Flask app with CORS configured
- [ ] Route to fetch weather from API
- [ ] Error handling (invalid city, API failures)
- [ ] Returns proper JSON format
- [ ] Test with Postman or Thunder Client

### Frontend
- [ ] Search input and button
- [ ] Display weather results dynamically
- [ ] Loading spinner/message while fetching
- [ ] Error message display
- [ ] Weather icons based on condition
- [ ] Responsive design
- [ ] Clean, appealing UI

### Integration
- [ ] Backend and frontend communicate properly
- [ ] No console errors
- [ ] Works for multiple city searches
- [ ] Handles edge cases (empty input, invalid cities)

---

## How to Run

### Terminal 1 (Backend)
```bash
cd backend
venv\Scripts\activate
python app.py
# Should run on http://localhost:5000
```

### Terminal 2 (Frontend)
```bash
cd frontend
# Option 1: Use Python simple server
python -m http.server 8000
# Option 2: Use Live Server extension in VS Code

# Open in browser: http://localhost:8000
```

---

## Important Notes

1. **API Key Security**: Never commit `.env` file with keys. Add to `.gitignore`
2. **CORS**: Backend must enable CORS for frontend to make requests
3. **Error Handling**: Handle cases like:
   - Empty city name
   - City not found
   - API rate limit exceeded
   - Network errors
4. **Testing**: Test with different cities, check console for errors
5. **UI/UX**: Make the app intuitive and visually appealing

---

## Free API Options (Pick One)

### Option 1: Open-Meteo (Recommended - No Key Needed)
```
https://api.open-meteo.com/v1/forecast?latitude=LATITUDE&longitude=LONGITUDE&current=temperature_2m
```

### Option 2: OpenWeatherMap
```
https://api.openweathermap.org/data/2.5/weather?q=CITY&appid=YOUR_API_KEY&units=metric
```

### Option 3: WeatherAPI
```
https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=CITY
```

---

## Submission Requirements
- [ ] Complete backend with proper error handling
- [ ] Complete frontend with dynamic updates
- [ ] Working weather API integration
- [ ] Clean, readable, commented code
- [ ] README with setup instructions
- [ ] No hardcoded API keys in code
- [ ] Responsive design
- [ ] All features working without errors

---

## Resources
- Flask Documentation: https://flask.palletsprojects.com/
- JavaScript Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- CSS Flexbox: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout
- Weather Icons: https://openweathermap.org/weather-conditions (or Font Awesome)

---

**Good luck! Build this step-by-step and test as you go.** 🌤️
