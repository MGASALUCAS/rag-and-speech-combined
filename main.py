import os
import uuid
from flask import Flask, render_template, send_file
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from gtts import gTTS
import pygame.mixer
from flask import request, jsonify
from gradio_client import Client
import speech_recognition as sr


# langchain imports
from dotenv import load_dotenv
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS


app = Flask(__name__)


# Function to generate and save the welcome message audio file
def generate_welcome_message():
    message = "Welcome to college of ICT receptionist. How can I help you"
    welcome_tts = gTTS(message, lang='en')
    welcome_tts.save("welcome.mp3")

def convert_text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")


@app.route('/speech-input', methods=['POST'])
def speech_input():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening for speech...")
            audio = recognizer.listen(source)
            print("Speech detected. Transcribing...")
            text = recognizer.recognize_google(audio)
            print("Transcribed text:", text)

            # Assuming the vectorstore has been created and saved previously
            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.load_local("vector_db", embeddings)

            # Set up the retrieval chain
            retriever = vectorstore.as_retriever()
            llm = ChatOpenAI()
            retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
            combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
            retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

            # Function to handle the question and get a response
            def get_response_from_question(question):
                response = retrieval_chain.invoke({"input": question})
                return response["answer"]

            # Example usage
            question = text
            response = get_response_from_question(question)
            print(response)

            result = response

            print(result)

            print("Prediction result:", result)
            convert_text_to_speech(result)
            pygame.mixer.init()
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            return jsonify({'message': 'Speech transcribed and prediction made successfully'})
    except sr.UnknownValueError:
        return jsonify({'error': 'Unable to transcribe speech'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/')
def index():
    welcome_message = "Welcome, this is University of Dar es Salaam co i ct reception. Please click the speaker and tell me what you need."
    if not os.path.exists("welcome.mp3"):
        generate_welcome_message()
    
    # Initialize pygame mixer and play the audio
    pygame.mixer.init()
    pygame.mixer.music.load("welcome.mp3")
    pygame.mixer.music.play()

    return render_template('index.html')

def text_to_speech_file(text: str) -> str:
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"static/{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

@app.route('/audio/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
