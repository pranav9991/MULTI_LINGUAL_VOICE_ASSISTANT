import streamlit as st
from src.helper import voice_input, llm_model_object, text_to_speech, store_pdf_in_db

def main():
    st.title("Multilingual AI Assistant 🤖")
    st.write("Upload Your PDF File!!")

    uploaded_file = st.file_uploader("Choose File", type="pdf")

    if uploaded_file is not None:
        with open("uploaded_file.pdf", "wb") as f:
            f.write(uploaded_file.read())

        store_pdf_in_db("uploaded_file.pdf")
        st.success("PDF successfully uploaded and stored!")

    st.write("Press the button below to start speaking. The assistant will listen to your voice input, process it, and generate a response.")
    
    if st.button("Ask Me Anything"):
        with st.spinner("Listening..."):
            user_text = voice_input()

            if user_text:
                response = llm_model_object(user_text)
                
                # Generate the speech from the response
                text_to_speech(response)
                
                # Open the correct audio file (response.mp3)
                audio_file = open("response.mp3", "rb")
                audio_bytes = audio_file.read()
                audio_file.close()

                # Display the response text and audio
                st.text_area(label="Response:", value=response, height=350)
                st.audio(audio_bytes)

                # Add a download button for the audio file
                st.download_button(
                    label="Download Speech",
                    data=audio_bytes,
                    file_name="response.mp3",  # Ensure the correct file name here
                    mime="audio/mp3"
                )
            else:
                st.error("No audio detected. Please try again.")

if __name__ == "__main__":
    main()
