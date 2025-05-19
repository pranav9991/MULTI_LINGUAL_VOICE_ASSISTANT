


# Multilingual AI Assistant 🤖

This is a Streamlit-based multilingual voice assistant app. It allows users to upload a PDF file, ask questions via voice, and receive intelligent responses generated using Google's Gemini LLM API. The assistant reads the response aloud and offers an audio download option.

---

## 🌟 Features

- 📄 Upload and store PDFs
- 🧠 Retrieval-Augmented Generation (RAG) over PDF content
- 🎤 Voice-based user input using microphone
- 💬 AI-generated response using Gemini LLM
- 🔊 Text-to-speech output using Google Text-to-Speech (gTTS)
- 📥 Downloadable `.mp3` audio of the AI’s response

---

## 🧠 How It Works

1. **Upload a PDF**: The document is stored and indexed using FAISS for RAG.
2. **Speak your question**: The app records audio and converts it to text.
3. **Generate response**: Gemini LLM generates a reply using the question and PDF context.
4. **Text-to-speech**: The response is converted to speech and played back.
5. **Download audio**: The `.mp3` file of the response can be downloaded.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <repo_url>
cd multilingual-ai-assistant
````

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For Windows users:

```bash
pipwin install pyaudio
```

### 4. Add your Google API Key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_google_gemini_api_key
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## 🗣️ How to Use

1. Open the web interface.
2. Upload a `.pdf` file.
3. Click on **"Ask Me Anything"**.
4. Speak into the microphone.
5. Listen to the assistant's voice reply.
6. Download the `.mp3` audio if desired.

---

## 📦 Local Installation

To install the package locally:

```bash
pip install -e .
```

---

## 👨‍💻 Author

**Pranav Parasar**
📧 [pranavparasar99@gmail.com](mailto:pranavparasar99@gmail.com)

---
