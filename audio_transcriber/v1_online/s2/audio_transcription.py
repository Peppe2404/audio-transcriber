import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
from pydub import AudioSegment
from pytube import YouTube
import os

# Funzione per il caricamento del file audio
def load_audio():
    file_path = filedialog.askopenfilename(filetypes=[("OGG files", "*.ogg")])
    if file_path:
        audio_path.set(file_path)

# Funzione per la trascrizione dell'audio
def transcribe_audio():
    file_path = audio_path.get()
    language = lang_var.get()

    if not file_path:
        messagebox.showerror("Errore", "Seleziona prima un file audio")
        return

    recognizer = sr.Recognizer()
    audio = AudioSegment.from_ogg(file_path)
    
    # Divide l'audio se più lungo di 3 minuti
    chunks = [audio[i:i + 180000] for i in range(0, len(audio), 180000)]
    full_text = ""

    for chunk in chunks:
        chunk_file = "temp_chunk.wav"
        chunk.export(chunk_file, format="wav")
        with sr.AudioFile(chunk_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language=language)
                full_text += text + " "
            except sr.UnknownValueError:
                full_text += "[Incomprensibile] "
            except sr.RequestError:
                messagebox.showerror("Errore", "Problema nella richiesta di trascrizione")
                return
        os.remove(chunk_file)

    # Mostra la trascrizione
    transcribe_window = tk.Toplevel(root)
    transcribe_window.title("Trascrizione")
    transcript_text = tk.Text(transcribe_window, wrap="word")
    transcript_text.insert("1.0", full_text)
    transcript_text.pack(expand=True, fill="both")

    def copy_text():
        root.clipboard_clear()
        root.clipboard_append(full_text)

    copy_button = tk.Button(transcribe_window, text="Copia Testo", command=copy_text)
    copy_button.pack()

# Funzione per scaricare l'audio da YouTube e convertirlo in WAV
def download_youtube_audio():
    url = yt_url.get()
    if not url:
        messagebox.showerror("Errore", "Inserisci prima un URL valido")
        return

    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        download_path = video.download()
        # Ottieni il percorso e il nome del file scaricato
        downloaded_file_path = download_path

        # Determina il formato del file scaricato
        if video.mime_type == "audio/webm":
            audio_format = "webm"
        else:
            audio_format = "mp4"

        # Converti il file scaricato in WAV
        audio = AudioSegment.from_file(downloaded_file_path, audio_format)
        wav_path = downloaded_file_path.split(".")[0] + ".wav"
        audio.export(wav_path, format="wav")
        os.remove(downloaded_file_path)
        audio_path.set(wav_path)
        messagebox.showinfo("Successo", "Download e conversione completati")
    except Exception as e:
        messagebox.showerror("Errore", "Errore nel download: " + str(e))

# Interfaccia grafica
root = tk.Tk()
root.title("Trascrittore Audio")

audio_path = tk.StringVar()
yt_url = tk.StringVar()
lang_var = tk.StringVar(value="it-IT")

# Sezione per il caricamento e la trascrizione del file audio
tk.Label(root, text="Seleziona File Audio:").pack()
tk.Entry(root, textvariable=audio_path, state="readonly").pack()
tk.Button(root, text="Carica", command=load_audio).pack()
tk.Label(root, text="Seleziona Lingua:").pack()
lang_menu = tk.OptionMenu(root, lang_var, "it-IT", "en-US")
lang_menu.pack()
tk.Button(root, text="Trascrivi", command=transcribe_audio).pack()

# Sezione per il download dell'audio da YouTube
tk.Label(root, text="Incolla URL YouTube:").pack()
tk.Entry(root, textvariable=yt_url).pack()
tk.Button(root, text="Scarica Audio", command=download_youtube_audio).pack()

root.mainloop()
