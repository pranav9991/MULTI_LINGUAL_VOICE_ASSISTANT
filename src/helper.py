import PyPDF2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import speech_recognition as sr
from gtts import gTTS
from google.generativeai import configure, GenerativeModel

# Load Sentence Transformer Model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# In-memory storage for document chunks
document_store = []

# Initialize FAISS index (using cosine similarity)
embedding_dimension = 384  # Dimension of 'all-MiniLM-L6-v2' model
index = faiss.IndexFlatL2(embedding_dimension)

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Store PDF text in FAISS
def store_pdf_in_db(pdf_path):
    pdf_text = extract_pdf_text(pdf_path)
    chunks = [pdf_text[i:i + 512] for i in range(0, len(pdf_text), 512)]  # Break into smaller chunks

    # Encode chunks into embeddings
    embeddings = sentence_model.encode(chunks)
    document_store.extend(chunks)  # Store the chunks in memory

    # Add embeddings to FAISS index
    index.add(np.array(embeddings))

# Retrieve relevant chunks based on the query
def retrieve_documents_from_pdf(query, n_results=3):
    query_embedding = sentence_model.encode([query])

    # Ensure the FAISS index has data
    if index.is_trained and index.ntotal > 0:
        # Search for similar embeddings in FAISS
        distances, indices = index.search(np.array(query_embedding), n_results)

        # Fetch the top matching chunks from the document store
        retrieved_docs = [document_store[idx] for idx in indices[0]]
        return retrieved_docs
    else:
        return ["No data available in FAISS index."]


# LLM model function (Gemini LLM)
def llm_model_object(user_text):
    try:
        # Retrieve relevant content from the PDF
        retrieved_docs = retrieve_documents_from_pdf(user_text)
        
        # Flatten the retrieved_docs list if needed
        retrieved_context = " ".join(
            [" ".join(doc) if isinstance(doc, list) else doc for doc in retrieved_docs]
        )

        # Combine the user query with the retrieved context
        combined_input = f"Context: {retrieved_context}\n\nUser Query: {user_text}"

        # Configure and use Gemini LLM
        configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = GenerativeModel('gemini-pro')

        # Generate a response
        response = model.generate_content(combined_input)
        return response.text
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        return "Sorry, there was an error processing your request."

# Voice input function
def voice_input():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        print("You said: ", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")
        return None

# Text-to-speech function
def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    tts.save("response.mp3")
    print("Response saved as response.mp3")

# Main function
def main():
    # Get voice input
    user_text = voice_input()

    # Generate LLM response with RAG
    if user_text:
        response = llm_model_object(user_text)
        print("AI Response: ", response)

        # Convert AI response to speech
        text_to_speech(response)

        # Play the audio response
        os.system("start response.mp3")  # On Windows; use 'open' for macOS, 'xdg-open' for Linux

if __name__ == "__main__":
    main()
