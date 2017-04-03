import sys
from abc import ABCMeta, abstractmethod
import os
import time

# Библиотеки распознавания и синтеза речи
import speech_recognition as sr
from gtts import gTTS

# Воспроизведение речи
import pyglet

# Библиотека Chatterbot для простого лингвистического ИИ
# https://github.com/gunthercox/ChatterBot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging

# Базовый класс
class ChatAI:

    __metaclass__=ABCMeta

    def __init__(self):
        
        self.bot = ChatBot(name="Robby",
            storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
            filters=["chatterbot.filters.RepetitiveResponseFilter"],
            database="./database.json"
        )

        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train("corpus", "chatterbot.corpus.russian")
        print("Обучение завершено")

    def work(self):

        self.pre_work()

        try:
            while True: 
                self.chat()

        except KeyboardInterrupt:
            # Сохраняем данные для следующей сессии
            # self.bot.trainer.export_for_training('corpus/last_session_corpus.json')
            self._clean_up()
            print("Пока!")

    # Ввод - генерация реплики - ответ
    @abstractmethod
    def chat(self):
        """ Прочитать ввод пользователя - сгенерировать ответ - ответить """
    
    # Подготовка
    @abstractmethod
    def pre_work(self):
        """ Какая-то подготовка... """

    # Генерация ответа
    def make_answer(self, statement):
        return self.bot.get_response(statement)




# Текстовая версия
class ChatAI_Text(ChatAI):

    def pre_work(self):
        """ Nothing do here """

    # Ввод - генерация реплики - ответ
    def chat(self):
        print('Вы: ', end='')
        statement = input()
        answer = self.make_answer(statement)
        print("{}: {}".format(self.bot.name, answer))

# Голосовая версия
class ChatAI_Speech(ChatAI):

    def __init__(self):
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._mp3_name = "speech.mp3"

        super(ChatAI_Speech, self).__init__()

    def pre_work(self):
        print("Минутку тишины, пожалуйста...")
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

    # Ввод - генерация реплики - ответ
    def chat(self):

        audio = self.listenInput()

        try:
            statement = self._recognizer.recognize_google(audio, language="ru_RU")        
            answer = self.make_answer(statement)
            # Союда можно добавить много интересностей (IoT, CV, ...)

            print("Вы: {}".format(statement))
            print("{}: {}".format(self.bot.name, answer))

            self.say(str(answer))

        except sr.UnknownValueError:
            print("Упс! Кажется, я тебя не понял")

        except sr.RequestError as e:
            print("Не могу получить данные от сервиса Google Speech Recognition; {0}".format(e))

    # Получение входной реплики
    def listenInput(self):
        print("Скажи что - нибудь!")
        with self._microphone as source:
            audio = self._recognizer.listen(source)

        print("Понял, идет распознавание...")
        return audio

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

    # Обработка аргументов командной строки
    if len(sys.argv) == 2 and sys.argv[1] == '-speech':  
        greeting()
        print('Speech mode\n\n')
        ai = ChatAI_Speech()

    elif len(sys.argv) == 2 and sys.argv[1] == '-text':
        greeting()
        print('Text mode\n\n')
        ai = ChatAI_Text()

    else:
        greeting()    
        print('Usage: python speech_ai.py -speech|-text')
        print('Mode:')
        print('  -speech - voice recognition and text-to-speech')
        print('  -text   - text chat in console')
        exit()

    ai.work()
    

main()