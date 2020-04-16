import speech_recognition as sr
import requests
import pydub
import os


def download(link):
    audio = requests.get(link)
    with open('audio_msg.mp3', 'wb') as f:
        f.write(audio.content)
        f.close()


def audio_convert():
    sound = pydub.AudioSegment.from_mp3('audio_msg.mp3')
    sound.export('audio_msg.wav', format='wav')
    os.remove('audio_msg.mp3')


def recognition():
    r = sr.Recognizer()
    file = 'audio_msg.wav'
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    try:
        print('I try recognition')
        text = r.recognize_google(audio)
        print('I do it')
        print(text)
        return text
    except:
        text = 'Я Вас, к сожалению не понял'
        return text
    finally:
        os.remove('audio_msg.wav')


def audio_answer(link):
    download(link)
    audio_convert()
    message = recognition()
    return message
