# Wejo Chatbot – Weather, Jokes, and Arithmetic

## 📌 Overview
Wejo is a simple chatbot powered by **FastAPI** that can:
- Provide weather information for cities or all states of a country.
- Tell programming and general jokes.
- Perform basic arithmetic operations.
- Run entirely locally with minimal setup.

---

## 🚀 Installation & Setup

### 1. Clone or Download
Place the project files in a directory:



my_chatbot/
├─__pycache__
├─ main.py
├─ README.md
└─ screenshots/
├─ chatbot_ui.png
└─joke_example.png
└─weather_example.png
└─ add_example.png


---

### 2. Install Dependencies
Make sure you have **Python 3.9+** installed, then run:

```bash
pip install fastapi uvicorn pydantic requests

3. Set Your API Keys

The chatbot uses:

OpenWeatherMap API → OPENWEATHER_API_KEY

GeoNames API → GEONAMES_USERNAME

Open main.py and update:

OPENWEATHER_API_KEY = "YOUR_API_KEY"
GEONAMES_USERNAME = "YOUR_USERNAME"

4. Run the Application
uvicorn main:app --reload


Visit in your browser:

http://127.0.0.1:8000/

💬 Example Queries
Weather
weather in India
weather in Chennai, Andhra Pradesh
weather in all states of India

Jokes
tell me a joke
joke about programming

Arithmetic
2+2
3*5
10/4
2^8
10%3

🎨 Features

Weather data fetched via OpenWeatherMap API.

Location data fetched via GeoNames API.

Jokes fetched via JokeAPI with a fallback joke list.

Animated chat bubble background colors.

Custom background image for the chat interface.