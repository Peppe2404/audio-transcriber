import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
from pydub import AudioSegment
import os

def convert_ogg_to_wav(ogg_file_path):
    """Convert OGG file to WAV format."""
    audio = AudioSegment.from_ogg(ogg_file_path)
    wav_file_path = ogg_file_path.replace('.ogg', '.wav')
    audio.export(wav_file_path, format="wav")
    return wav_file_path

def select_audio_file():
    file_path = filedialog.askopenfilename()
    return file_path

def transcribe_audio(file_path, language):
    recognizer = sr.Recognizer()
    # Convert OGG to WAV if needed
    if file_path.endswith(".ogg"):
        file_path = convert_ogg_to_wav(file_path)
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)
        return text

def main():
    window = tk.Tk()
    window.title("Audio Transcription")

    tk.Label(window, text="Select Language:").pack()
    lang_var = tk.StringVar(value="en-US")
    tk.Radiobutton(window, text="English", variable=lang_var, value="en-US").pack()
    tk.Radiobutton(window, text="Italian", variable=lang_var, value="it-IT").pack()

    tk.Button(window, text="Select Audio File and Transcribe", command=lambda: print(transcribe_audio(select_audio_file(), lang_var.get()))).pack()

    window.mainloop()

if __name__ == "__main__":
    main()
