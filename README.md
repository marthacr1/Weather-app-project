# ⛅ Skyveil — Weather Forecast App

A clean, real-time weather forecast web app built with **Python + Flask** and the **OpenWeatherMap API**.

## Features

- 🌡️ Current temperature, feels-like, humidity, wind, visibility & pressure
- 📅 5-day daily forecast with icons
- 🎨 Responsive, dark-themed UI
- ⚡ Fast — single API key, two endpoint calls

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/weather-forecast-app.git
cd weather-forecast-app
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
```bash
cp .env.example .env
# Edit .env and paste your OpenWeatherMap API key
```

Get a free key at [openweathermap.org/api](https://openweathermap.org/api).

### 5. Run the app
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

```
weather-forecast-app/
├── app.py               # Flask backend & API logic
├── requirements.txt
├── .env.example
├── templates/
│   └── index.html       # Single-page frontend
└── static/
    ├── css/style.css
    └── js/main.js
```

## Deployment

For production, run with Gunicorn:
```bash
gunicorn app:app
```

## License

MIT
