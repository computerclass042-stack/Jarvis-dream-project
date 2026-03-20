import pywhatkit as kit # Sabse upar add karein
import os
import pyautogui
from PIL import Image
from google import genai
from groq import Groq
import speech_recognition as sr
import win32com.client
import webbrowser  # Naya import links kholne ke liye

# --- Clients Setup ---
groq_client = Groq(api_key="")
gemini_client = genai.Client(api_key="")
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def speak(text):
    print("Jarvis:", text)
    speaker.Speak(text)

# --- 🧠 Brain (Groq - Smart URL Logic) ---
def get_groq_response(user_input):
    try:
        # Humne prompt mein instructions di hain ki websites ke liye sirf URL de
        system_prompt = (
            "You are Jarvis. Keep responses short and professional. Sir is a trader and programmer. "
            "IMPORTANT: If the user asks to open a website or tab, respond ONLY with the direct URL (e.g., https://google.com). "
            "Do not add any extra text if providing a URL."
        )
        
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content.strip()
    except:
        return "I'm having trouble thinking, sir."

# --- 👁️ Eyes (Gemini - Vision) ---
def analyze_screen():
    path = "screen_capture.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    speak("Analyzing your screen, sir...")
    
    img = Image.open(path)
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=["Analyze this screen. If it's a trading chart, tell me the trend. If it's code, find errors.", img]
        )
        return response.text
    except Exception as e:
        return f"Vision error: {e}"

# --- 🛠️ Logic Controller ---
def process_logic(c):
    c = c.lower()
    
    # 1. Screen Vision
    if "look at my screen" in c or "screen dekho" in c:
        result = analyze_screen()
        speak(result)
        return

    # 2. Get Brain Response (Groq)
    reply = get_groq_response(c)

    # 3. Smart Tab Opener Logic
    # Agar response "http" se start hota hai, toh browser mein kholo
    if reply.startswith("http"):
        speak(f"Opening requested tab, sir.")
        webbrowser.open(reply)
    else:
        # Baaki sab normal baaton ke liye
        speak(reply)
def process_logic(c):
    c = c.lower()
    
    # --- WhatsApp Logic ---
    if "whatsapp" in c and "message" in c:
        speak("Whom should I message, sir? Please tell me the phone number with country code.")
        # Aap yahan number aur message bhi voice se le sakte hain
        # Example logic:
        # kit.sendwhatmsg_instantly("+91XXXXXXXXXX", "Hello Sir, Jarvis here!")
        speak("Sir, for now I can open the web tab, but to send a specific text, we need to integrate your contact list.")
        webbrowser.open("https://web.whatsapp.com")
        return

    # --- Baaki Brain Logic ---
    reply = get_groq_response(c)
    if reply.startswith("http"):
        speak("Opening requested tab, sir.")
        webbrowser.open(reply)
    else:
        speak(reply)
# --- Main Loop ---
if __name__ == "__main__":
    speak("Jarvis is online with Vision and Brain.")
    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1 # Thoda wait karega user ke bolne ka
            print("Listening...")
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=9)
                command = r.recognize_google(audio)
                print(f"You: {command}")
                
                if "exit" in command.lower():
                    speak("System shutting down. Goodbye sir.")
                    break
                
                process_logic(command)
            except:
                continue