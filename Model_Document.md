Model Document: NLP Approach & Rationale
1. Overview

This project implements a lightweight chatbot API using FastAPI with simple NLP-based intent detection.
It supports:

Weather queries (city, or all states in a country)

Joke retrieval

Basic arithmetic

Fallback for unrecognized queries

Instead of using a heavy NLP model, it relies on string pattern matching and minimal text preprocessing to detect intents.

2. NLP Approach
2.1 Preprocessing

Lowercasing
All input is converted to lowercase to make matching case-insensitive.

Whitespace trimming
Leading/trailing spaces are removed.

Example:
"Weather in London" → "weather in london"

2.2 Intent Detection

The detect_intent_and_route() function determines intent by checking keywords and phrases:

Weather for all states
Condition: "weather" in message and "all states of" in message

Extracts the country name after "all states of".

Calls detect_country_code() → get_states_of_country() → get_weather() for each state.

Weather for specific cities
Condition: "weather" in message (without "all states of")

Removes "weather" / "weather in" to isolate city names.

Splits by commas to handle multiple cities.

Fetches weather for each city.

Jokes
Condition: "joke" in message

Calls getJoke() which queries jokeapi.dev or returns a random fallback.

Arithmetic
Condition: any of +, -, *, /, ^, % in message

Replaces ^ with Python’s ** for exponentiation.

Uses eval() in a try/except to compute results safely.

Fallback
If no rules match, returns "Sorry, I couldn't understand your request."

2.3 API Calls

Weather Data:
OpenWeatherMap API (current temperature + description).

Geographical Data:
GeoNames API for country codes & administrative divisions (states).

Jokes:
JokeAPI with blacklist filters for clean content.

3. Rationale for the Approach
3.1 Simplicity

The system avoids heavyweight NLP models (e.g., BERT, spaCy) to ensure fast, low-resource execution.

Keyword-based matching is sufficient for the small, clearly defined domain.

3.2 Transparency

The logic is explicit and easy to extend.
Adding new intents only requires adding more if conditions.

3.3 Speed

No model loading time.

API response is near-instant for most queries.

3.4 Control

Keyword rules prevent ambiguous results that statistical models might produce for short queries.

4. Limitations

Rigid phrasing: User must use specific keywords ("weather", "joke", operators).

No contextual understanding: Cannot handle complex or implicit requests like "How's the temperature in Tokyo right now?" unless the keyword "weather" is present.

Eval() risk: Although limited, eval() could pose security concerns if not sandboxed.

5. Possible Improvements

Replace hardcoded keyword matching with NLU libraries like Rasa NLU or spaCy for more flexible intent recognition.

Add entity extraction to handle city/country names without rigid string parsing.

Use regex-based parsing for arithmetic to validate expressions before evaluating.

Implement conversation context so follow-up questions make sense.

In summary:
This chatbot uses a rule-based NLP approach — a deliberate trade-off for speed, simplicity, and ease of maintenance in a constrained use case. It’s well-suited for demos, prototypes, or small-scale personal assistants, but could evolve into a more robust NLU-powered system with additional features.