import speech_recognition as sr
import requests
import pydub
import os


# скачивает и записывает на диск аудио сообщение
def download(link):
    audio = requests.get(link)
    with open('audio_msg.mp3', 'wb') as f:
        f.write(audio.content)
        f.close()


# конвертирует запись в мр3
def audio_convert():
    sound = pydub.AudioSegment.from_mp3('audio_msg.mp3')
    sound.export('audio_msg.wav', format='wav')
    os.remove('audio_msg.mp3')


# распознование
def recognition():
    # создаем класс
    r = sr.Recognizer()
    file = 'audio_msg.wav'
    # читаем файл
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    # пробуем распознать
    try:
        print('Пробую распознать')
        text = r.recognize_google(audio, language='ru_RU')
        print('Google думает, что в записи сказано:' + text)
        return text
    except:
        print('Распознавание не удалось')
    finally:
        os.remove('audio_msg.wav')


# функция для импорта
def audio_answer(link):
    download(link)
    audio_convert()
    return recognition()
