import sys

# Библиотеки распознавания и синтеза речи
import speech_recognition as sr
from gtts import gTTS

# Воспроизведение речи
import pyglet

import os
import time

# Библиотека Chatterbot для простого лингвистического ИИ
# https://github.com/gunthercox/ChatterBot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

class Speech_AI:
    def __init__(self, speech = False):
        self._speech = speech

        if self._speech:
            self._recognizer = sr.Recognizer()
            self._microphone = sr.Microphone()
            self._mp3_name = "speech.mp3"

        self.bot = ChatBot(name="Robby",
            storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
            filters=["chatterbot.filters.RepetitiveResponseFilter"],
            database="./database.json"
        )

        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train("corpus", "chatterbot.corpus.russian")
        print("Обучение завершено")

    def work(self):

        if self._speech:
            print("Минутку тишины, пожалуйста...")
            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source)

        try:
            while True:

                if self._speech:
                    audio = self.listenInput()

                try:

                    if self._speech:
                        statement = self._recognizer.recognize_google(audio, language="ru_RU")
                    else:
                        statement = input()

                    answer = self.chat(statement)

                    if self._speech:
                        self.say(str(answer))

                except sr.UnknownValueError:
                    print("Упс! Кажется, я тебя не понял")

                except sr.RequestError as e:
                    print("Не могу получить данные от сервиса Google Speech Recognition; {0}".format(e))

        except KeyboardInterrupt:
            # Сохраняем данные для следующей сессии
            # self.bot.trainer.export_for_training('corpus/last_session_corpus.json')
            self._clean_up()
            print("Пока!")


    # Получение входной реплики
    def listenInput(self):
        print("Скажи что - нибудь!")
        with self._microphone as source:
            audio = self._recognizer.listen(source)

        print("Понял, идет распознавание...")
        return audio

    # Генерация реплики - ответ
    def chat(self, statement):
        answer = self.make_answer(statement)
        # Союда можно добавить много интересностей (IoT, CV, ...)

        print("Вы сказали: {}".format(statement))
        print("{} сказал: {}".format(self.bot.name, answer))
        return answer

    # Генерация ответа
    def make_answer(self, statement):
        return self.bot.get_response(statement)

    #Текст-в-речь и воспроизведение
    def say(self, phrase):
        tts = gTTS(text=phrase, lang="ru")
        tts.save(self._mp3_name)
        self.playMp3(self._mp3_name)
        
    def playMp3(self, filename):
        player = pyglet.media.Player()
        music = pyglet.resource.media(filename)
        player.queue(music)
        player.play()
        
        # Ожидаем конца воспроизведения
        while True:
            time.sleep(0.1)        
            if player.time == 0:
                break;

    def _clean_up(self):
        def clean_up():
            os.remove(self._mp3_name)


def greeting():
    print('**********************************')
    print('* Welcome to Speech AI chat-bot! *')
    print('**********************************')

def main():

    print(sys.argv)

    # Обработка аргументов командной строки
    if len(sys.argv) == 2 and sys.argv[1] == '-speech':  
        greeting()
        print('Speech mode')
        ai = Speech_AI(True)
        ai.work()

    elif len(sys.argv) == 2 and sys.argv[1] == '-text':
        greeting()
        print('Text mode')
        ai = Speech_AI(False)
        ai.work()

    else:
        greeting()    
        print('Usage: python speech_ai.py -speech|-text')
        print('Mode:')
        print('  -speech - voice recognition and text-to-speech')
        print('  -text   - text chat in console')
        exit()


    

main()