from setuptools import find_packages, setup

setup(
    name="AI Assistant",
    version="0.0.0",
    author="Pranav Parasar",
    author_email="pranavparasar99@gmail.com",
    packages=find_packages(),
    install_requires=[
    "SpeechRecognition",
    "pipwin",
    "pyaudio",
    "gTTS",
    "google-generativeai",
    "python-dotenv",
    "streamlit",
    "PyPDF2",
    "faiss-cpu",
    "sentence-transformers"
]
)