import speech_recognition as sr
import pywhatkit
import webbrowser
import datetime
import pyttsx3
import pyjokes
import os
import sys
import wikipedia
import requests
from geopy.geocoders import Nominatim
 

def speak(text,voice="Samantha"):
    try:
        os.system(f'say -v {voice} "{text}"')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    
    except Exception as e:
        print(e)
        print("Say that Again please...")
        speak("Say that Again please...")
        return "None"
    return query.lower()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")
    
    speak("I am Jarvis 2 point o , Please tell me how may I help you")


def get_weather_info(city_name):
    try:
        # Use geolocation to get coordinates for the city
        geolocator = Nominatim(user_agent="geoapiExercies")
        location = geolocator.geocode(city_name)
        
        if location:
            latitude = location.latitude
            longitude = location.longitude
            api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=1928ae6351f01c8101d0d28c6602e2e4"
            
            response = requests.get(api_url)
            weather_data = response.json()
            
            if weather_data.get('cod') == 200:
                weather_description = weather_data['weather'][0]['description']
                temperature = int(weather_data['main']['temp']-273.15)
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                
                # Format and speak the weather information
                speak(f"In {city_name}, the weather is {weather_description}.")
                speak(f"The temperature is {temperature} degrees Celsius.")
                speak(f"Humidity is {humidity}% and wind speed is {wind_speed} meters per second.")
            else:
                speak("Sorry, I couldn't fetch the weather information for that city.")
        else:
            speak(f"Sorry, I couldn't find the coordinates for {city_name}.")
    except Exception as e:
        speak(f"An error occurred: {e}")

news_api_key = '71471099c5de4b3a8deeec41f9221492'

def get_news(limit=3):
    try:
        api_url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
        response = requests.get(api_url)

        if response.status_code == 200:
            news_data = response.json()

            if 'articles' in news_data:
                articles = news_data['articles']
                if articles:
                    speak("Here are the latest news headlines:")
                    for article in articles:
                        title = article.get('title', 'No title available')
                        speak(title)
                else:
                    speak("Sorry, I couldn't find any news headlines at the moment.")
            else:
                speak("Sorry, I couldn't fetch news headlines at the moment.")
        else:
            speak(f"Failed to fetch news. HTTP Status Code: {response.status_code}")

    except Exception as e:
        speak(f"An error occurred: {e}")

def respond_to_joke(query):
    joke = pyjokes.get_joke()
    speak(joke)
    print(joke)
    while True:
        response = takeCommand()
        if 'ha ha' in response:
            speak("I'm glad you found it funny!")
        else:
            speak("I'm here to tell jokes. If you have any other requests, feel free to ask.")
        break


if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], 
                 ["wikipedia", "https://www.wikipedia.com"],
                   ["google", "https://www.google.com"],
                   ["chat gpt", "https://chat.openai.com"],
                   ]
        
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if 'play' in query:
            song = query.replace('play', '')
            speak('playing ' + song)
            pywhatkit.playonyt(song)

        elif 'wikipedia' in query:
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.PageError:
                speak(f"Sorry, I couldn't find any information on '{query}' on Wikipedia.")
            except Exception as e:
                speak(f"An error occurred: {e}")

        elif 'time' in query:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak('Current time is ' + time)

        elif 'date' in query:
            current_date = datetime.datetime.now().strftime('%B %d, %Y')
            speak('Today is ' + current_date)

        elif 'open code' in query:
            codePath = "C:\\Users\\Dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'are you single' in query:
            speak('I am in a relationship with wifi')

        elif 'what can you do' in query:
            speak('I can play your favourite song on youtube , tell the weather of any city you want to know , read top news headlines , can answer anything from wikipedia , tell some funny jokes and many more ')

        elif 'who are you' in query:
            speak('I am Jarvis , a virtual assistant created by beebake car key')

        elif 'i love you' in query:
            speak('Hiye may... mar. jawa!!')

        elif 'joke' in query:
            respond_to_joke(query)

        elif 'calculate' in query:
            expression = query.replace('calculate', '').strip()
            expression = expression.replace('x', '*').replace('times', '*') 
            try:
                result = eval(expression)
                speak(f"The result of {expression} is {result}")
            except Exception as e:
                speak("Sorry, I couldn't calculate that.")

        if 'weather' in query:
            city_name = query.replace('weather', '').strip()
            get_weather_info(city_name)

        elif 'news' in query:
            get_news(limit=3)

        elif 'jarvis stop' in query or 'exit jarvis' in query:
            speak("Thank you for using Jarvis! Have a great day! Goodbye!")
            sys.exit()

        