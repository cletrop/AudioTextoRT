import pyaudio
import wave
import threading

from google.cloud import speech
import os
import io

#setting Google credential
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= 'ministerio-vino-y-aceite-1dcf294b1b7c.json'
client = speech.SpeechClient()

FORMAT = pyaudio.paInt16 #posiblemente haya que cambiar esto a int32
CHANNELS = 1
RATE = 44100
CHUNK = 4410
RECORD_SECONDS = 15

count_audio = 0

def UploadAudio(file_name):
  with io.open(file_name, "rb") as audio_file:
      content = audio_file.read()
      audio = speech.RecognitionAudio(content=content)

  config = speech.RecognitionConfig(
      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
      enable_automatic_punctuation=True,
      audio_channel_count=CHANNELS,
      language_code="es",
  )

  # Sends the request to google to transcribe the audio
  response = client.recognize(request={"config": config, "audio": audio})
  # Reads the response
  for result in response.results:
      print("Transcript: {}".format(result.alternatives[0].transcript))

  try:
    os.remove(file_name)
    print(f"El archivo '{file_name}' ha sido eliminado correctamente.")
  except OSError as e:
    print(f"No se pudo eliminar el archivo '{file_name}': {e}")

while True:
  audio = pyaudio.PyAudio()
  file_name = "audio{0}.wav".format(count_audio)
  # Abre un flujo de audio
  stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

  frames = []

  # Grabar datos del flujo de audio
  for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

  # Detiene y cierra el flujo del audio
  stream.stop_stream()
  stream.close()
  audio.terminate()

  # Guarda los datos grabados en un archivo WAV
  wf = wave.open(file_name, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(audio.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))
  wf.close()

  upload_thread = threading.Thread(target=UploadAudio, args=(file_name,))
  upload_thread.start()
  
  count_audio = count_audio + 1


