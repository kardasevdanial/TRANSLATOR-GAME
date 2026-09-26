import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

duration = 6  # секунды записи
sample_rate = 44100
lives = 3
words_by_level = {
    "easy": ["кот", "собака", "печенье", "молоко", "солнце"],
    "medium": ["банан", "школа", "друг", "окно", "жёлтый"],
    "hard": ["технология", "университет", "информация", "произношение", "воображение"]
}
print("Здраствуйте! В этой игре будут показаны слова на русском языкеб а вы должны произнести их на английском.")

recognized = input("Введите сложность (easy, medium, hard): ")
recognized = recognized.lower()

while True:

    word = random.choice(words_by_level[recognized])
    print(word)
    
    print("Говори...")
    recording = sd.rec(
        int(duration * sample_rate), # длительность записи в сэмплах
        samplerate=sample_rate,      # частота дискретизации
        channels=1,                  # 1 — это моно
        dtype="int16")               # формат аудиоданных
    sd.wait()  # ждём завершения записи

    wav.write("output.wav", sample_rate, recording)

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en")
        print("Ты сказал:",text)
        translator = Translator()
        translated = translator.translate(word, dest='en')  # здесь 'en' — это английский
        if translated.text.lower() == text.lower():
            print("Молодец! Ты перевел(а) слово правильно!")
        else:
            print("Нет! Ты перевел не правильно! Вот правильный перевод: ",translated.text)
            lives -= 1
        sledushiy_raund = input("Двигаемся далше? ( Да / Нет ) ")
        if sledushiy_raund == "Да":
            print("Хорошо!")
        elif sledushiy_raund =="Нет":
            print("Игра окончена!")
            break
        else:
            print("Вы ввели что то непонятное! ( я не знаю как вернуть вас обратно на вопрос так что игра окончена) )")
            break
        if lives == 0:
            break
    except sr.UnknownValueError:             # - если Google не понял речь (шум, молчание)
        print("Не удалось распознать речь.")
    except sr.RequestError as e:             # - если нет интернета или API недоступен
        print(f"Ошибка сервиса: {e}")
    
    
if lives == 0:
    print("У вас закончились жизни!")


