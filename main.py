from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests, random
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENWEATHER_API_KEY = "7c0cea712245467bf6756b45a0965e0b"
GEONAMES_USERNAME = "anjani_98"

def getJoke() -> str:
    try:
        url = (
            "https://v2.jokeapi.dev/joke/"
            "Programming,Miscellaneous,Pun,Spooky,Christmas"
            "?blacklistFlags=nsfw,racist,sexist,explicit"
        )
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            joke_data = r.json()
            if joke_data.get("type") == "single":
                return joke_data.get("joke", "Couldn't fetch a joke right now.")
            elif joke_data.get("type") == "twopart":
                return f"{joke_data.get('setup', '')} {joke_data.get('delivery', '')}"
        return random.choice([
            "Why don't skeletons fight each other? They don't have the guts!",
            "I told my wife she should embrace her mistakes. She gave me a hug.",
            "Why was the math book sad? Because it had too many problems.",
            "I only know 25 letters of the alphabet. I don't know y.",
            "What do you call fake spaghetti? An impasta!",
            "I asked my dog what's two minus two. He said nothing."
        ])
    except:
        return "Couldn't fetch a joke right now."

def get_states_of_country(country_code):
    url = f"http://api.geonames.org/searchJSON?country={country_code}&featureCode=ADM1&maxRows=50&username={GEONAMES_USERNAME}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return []
    data = resp.json()
    return [item["name"] for item in data.get("geonames", [])]

def get_weather(city_name, country_code=""):
    query = f"{city_name},{country_code}" if country_code else city_name
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={OPENWEATHER_API_KEY}&units=metric"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    return resp.json()

def detect_country_code(country_name):
    url = f"http://api.geonames.org/searchJSON?q={country_name}&maxRows=1&featureClass=A&username={GEONAMES_USERNAME}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    if data.get("geonames"):
        return data["geonames"][0]["countryCode"]
    return None

def detect_intent_and_route(message):
    message = message.strip().lower()

    # Weather in all states of a country
    if "weather" in message and "all states of" in message:
        country_name = message.split("all states of", 1)[1].strip()
        country_code = detect_country_code(country_name)
        if not country_code:
            return {"result": f"Could not find country '{country_name}'."}
        states = get_states_of_country(country_code)
        if not states:
            return {"result": f"Could not find states for '{country_name}'."}
        output_lines = []
        for state in states:
            w = get_weather(state, country_code)
            if w:
                output_lines.append(f"{state}: {w['main']['temp']}°C, {w['weather'][0]['description']}")
            else:
                output_lines.append(f"{state}: Not found")
        return {"result": "\n".join(output_lines)}

    # General weather queries (any position)
    if "weather" in message:
        # Extract city names by removing "weather" or "weather in"
        cities_str = (
            message.replace("weather in", "")
                   .replace("weather", "")
                   .strip()
        )
        if not cities_str:
            return {"result": "Please tell me the city name after 'weather'."}
        cities = [c.strip() for c in cities_str.split(",") if c.strip()]
        output_lines = []
        for city in cities:
            w = get_weather(city)
            if w:
                output_lines.append(f"{city}: {w['main']['temp']}°C, {w['weather'][0]['description']}")
            else:
                output_lines.append(f"{city}: Not found")
        return {"result": "\n".join(output_lines)}

    # Jokes
    if "joke" in message:
        return {"result": getJoke()}

    # Arithmetic
    if any(op in message for op in ["+", "-", "*", "/", "^", "%"]):
        try:
            expr = message.replace("^", "**")
            result = eval(expr)
            return {"result": f"The answer is {result}"}
        except:
            return {"result": "Sorry, I couldn't calculate that."}

    return {"result": "Sorry, I couldn't understand your request."}

class QueryRequest(BaseModel):
    query: str

CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Simple API Router Chat</title>
  <style>
    body { font-family: Arial, sans-serif; background:#f4f6f8; display:flex; justify-content:center; padding-top:50px; }
    .chat-container { background:#fff; width:420px; border-radius:10px; box-shadow:0 4px 10px rgba(0,0,0,.1); display:flex; flex-direction:column; }
    .chat-header { background:#0078d4; color:#fff; padding:15px; border-radius:10px 10px 0 0; font-weight:bold; font-size:18px; text-align:center; }
    .chat-box { padding:12px; height:360px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; }
    .chat-message { padding:10px; border-radius:8px; max-width:75%; word-wrap:break-word; white-space:pre-line; }
    .chat-message.user { background:#daf8cb; align-self:flex-end; }
    .chat-message.bot { background:#e6e6e6; align-self:flex-start; }
    .chat-input-area { display:flex; border-top:1px solid #ddd; }
    .chat-input-area input { border:none; padding:12px; flex-grow:1; font-size:16px; }
    .chat-input-area button { background:#0078d4; color:#fff; border:none; padding:10px 15px; cursor:pointer; font-size:16px; }
    .chat-input-area button:hover { background:#005ea0; }
  </style>
</head>
<body>
  <div class="chat-container">
    <div class="chat-header">Wejo</div>
    <div id="chatBox" class="chat-box"></div>
    <div class="chat-input-area">
<input id="queryInput" placeholder="Ask me about weather, jokes or Arithmetic operations..." onkeypress="if(event.key==='Enter') send()" />
      <button onclick="send()">Send</button>
    </div>
  </div>
  <script>
    const chatBox = document.getElementById('chatBox');
    function addMessage(text, who){
      const d=document.createElement('div');
      d.className='chat-message '+who;
      d.innerText = text;
      chatBox.appendChild(d);
      chatBox.scrollTop=chatBox.scrollHeight;
    }
    async function send(){
      const input = document.getElementById('queryInput');
      const q = input.value.trim();
      if(!q) return;
      addMessage(q,'user'); input.value='';
      try{
        const r = await fetch('/process_query',{method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({query:q})});
        const data = await r.json();
        addMessage(data.result || data.error || 'No response', 'bot');
      }catch(e){ addMessage('Request failed. Is the server running?', 'bot'); }
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(CHAT_HTML)

@app.post("/process_query")
async def process_query(payload: QueryRequest):
    return detect_intent_and_route(payload.query)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
