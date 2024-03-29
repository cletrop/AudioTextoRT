import pyaudio
import wave
import whisper
import os
import numpy

FORMAT = pyaudio.paInt16 #posiblemente haya que cambiar esto a int32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio.wav"

audio = pyaudio.PyAudio()

# Abre un flujo de audio
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("Grabando")

frames = []

# Grabar datos del flujo de audio
for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
  data = stream.read(CHUNK)
  frames.append(data)

print("Grabación finalizada")

# Detiene y cierra el flujo del audio
stream.stop_stream()
stream.close()
audio.terminate()

# Guarda los datos grabados en un archivo WAV
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_del_archivo = os.path.join(directorio_actual, WAVE_OUTPUT_FILENAME)
f = open(ruta_del_archivo)

print(ruta_del_archivo)

# if(audioExist == True):
model = whisper.load_model("medium")
result = model.transcribe(audio=WAVE_OUTPUT_FILENAME, fp16=False, language="es")

print(result["text"])