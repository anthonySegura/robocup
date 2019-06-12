#speech.py
import pyaudio
import wave
import requests
import json
import serial 
import time

API_ENDPOINT = 'https://api.wit.ai/speech'
ACCESS_TOKEN = '3ZGSGWG2Q4DE4JUH3CBMGPVOUYVVUHL4'
#ser = serial.Serial('COM7', 9600)

def record_audio(RECORD_SECONDS, WAVE_OUTPUT_FILENAME):
    #--------- SETTING PARAMS FOR OUR AUDIO FILE ------------#
    FORMAT = pyaudio.paInt16    # format of wave
    CHANNELS = 1                # no. of audio channels
    RATE = 44100                # frame rate
    CHUNK = 1024                # frames per audio sample
    #--------------------------------------------------------#

    # creating PyAudio object
    audio = pyaudio.PyAudio()

    # open a new stream for microphone
    # It creates a PortAudio Stream Wrapper class object
    stream = audio.open(format=FORMAT,channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    #----------------- start of recording -------------------#
    print("Listening...")

    # list to save all audio frames
    frames = []

    for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
        # read audio stream from microphone
        data = stream.read(CHUNK)
        # append audio data to frames list
        frames.append(data)

    #------------------ end of recording --------------------#   
    print("Finished recording.")

    stream.stop_stream()    # stop the stream object
    stream.close()          # close the stream object
    audio.terminate()       # terminate PortAudio

    #------------------ saving audio ------------------------#

    # create wave file object
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')

    # settings for wave file object
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))

    # closing the wave file object
    waveFile.close()

def read_audio(WAVE_FILENAME):
    # function to read audio(wav) file
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio

def RecognizeSpeech(AUDIO_FILENAME, num_seconds = 5):

    # record audio of specified length in specified audio file
    record_audio(num_seconds, AUDIO_FILENAME)

    # reading audio
    audio = read_audio(AUDIO_FILENAME)

    # WIT.AI HERE
    # ....
    # get a sample of the audio that we recorded before. 
    audio = read_audio("myspeech.wav")

    # defining headers for HTTP request
    headers = {'authorization': 'Bearer ' + ACCESS_TOKEN,
            'Content-Type': 'audio/wav'}

    #Send the request as post request and the audio as data
    resp = requests.post(API_ENDPOINT, headers = headers,
                            data = audio)

    #Get the text
    data = json.loads(resp.content)
    print(data)
    Move(data["_text"])

def Move(arg):
    instruction = ''
    if(arg == 'up'):
        instruction = 'F'
    elif(arg == 'down'):
        instruction = 'B'
    elif(arg == 'right'):
        instruction = 'R'
    elif(arg == 'left'):
        instruction = 'L'
    else:
        instruction = 'I'
    #ser.write(str.encode(instruction))
    print(instruction)

def start_listening():
    count = 1
    while True:
         print(count)
         count += 1
         time.sleep(0.1) # Necesario para que python no mate al hilo, probar con diferentes tiempos
         #text = RecognizeSpeech('myspeech.wav', 4)

# if __name__ == "__main__":
#     while True:
#         text =  RecognizeSpeech('myspeech.wav', 4)
