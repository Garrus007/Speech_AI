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
    def __init__(self):
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

        self.bot = ChatBot(name="Robby",
            storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
            filters=["chatterbot.filters.RepetitiveResponseFilter"],
            database="./database.json"
        )

        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train("corpus", "chatterbot.corpus.russian")
        print("Обучение завершено")

        self._mp3_name = "speech.mp3"

    def work(self):
        print("Минутку тишины, пожалуйста...")
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

        try:
            while True:
                print("Скажи что - нибудь!")
                with self._microphone as source:
                    audio = self._recognizer.listen(source)
                print("Понял, идет распознавание...")
                try:
                    statement = self._recognizer.recognize_google(audio, language="ru_RU")

                    answer = self.make_answer(statement)
                    # Союда можно добавить много интересностей (IoT, CV, ...)

                    print("Вы сказали: {}".format(statement))
                    print("{} сказал: {}".format(self.bot.name, answer))

                    self.say(str(answer))

                except sr.UnknownValueError:
                    print("Упс! Кажется, я тебя не понял")

                except sr.RequestError as e:
                    print("Не могу получить данные от сервиса Google Speech Recognition; {0}".format(e))

        except KeyboardInterrupt:
            # Сохраняем данные для следующей сессии
            self.bot.trainer.export_for_training('corpus/last_session_corpus.json')
            self._clean_up()
            print("Пока!")

    def say(self, phrase):
        tts = gTTS(text=phrase, lang="ru")
        tts.save(self._mp3_name)
        self.playMp3(self._mp3_name)
        

    def playMp3(self, filename):
        player = pyglet.media.Player()
        music = pyglet.resource.media(filename)
        player.queue(music)
        player.play()
    
        while True:
            time.sleep(0.1)        
            if player.time == 0:
                break;

    def make_answer(self, statement):
        return self.bot.get_response(statement)

    def _clean_up(self):
        def clean_up():
            os.remove(self._mp3_name)


def stop():
    print('stop')

def main():
    ai = Speech_AI()
    ai.work()

main()