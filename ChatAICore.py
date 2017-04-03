from abc import ABCMeta, abstractmethod

# Библиотека Chatterbot для простого лингвистического ИИ
# https://github.com/gunthercox/ChatterBot
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
#import logging


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