import vk_requests
import ChatAICore
import time
import VkSettings

class ChatAI_VK(ChatAICore.ChatAI):

	def __init__(self, app_id, login, password, chat_id):
		self.app_id = app_id
		self.login = login
		self.password = password
		self.chat_id = chat_id

		self.api = vk_requests.create_api(app_id=self.app_id, login=self.login, password=self.password, scope=['messages '])

		me = self.api.users.get()[0]
		self.my_id = me['id']
		self.last_message_id = ''

		super(ChatAI_VK, self).__init__()

	def pre_work(self):
		"""wtf"""

	def chat(self):
		last_message = self.api.messages.getHistory(user_id=self.chat_id, count='1')['items'][0]

		if last_message['from_id'] != self.my_id and last_message['id'] != self.last_message_id:
			self.last_message_id = last_message['from_id']
			user_name = self.getUserName(last_message['from_id'])
			
			statement = last_message['body']

			if statement=='':
				time.sleep(1)
				return

			answer = self.make_answer(statement)

			print("{}: {}".format(user_name, statement))
			print("Бот: {}".format(answer))
			self.sendMessage("БОТ: {}".format(answer))

		time.sleep(1)

	def sendMessage(self, text):
		self.api.messages.send(user_id=self.chat_id, message=text)

	def getUserName(self, id):
		user = self.api.users.get(users_id=id)[0]
		return "{} {}".format(user['first_name'], user['last_name'])


ai = ChatAI_VK(VkSettings.app_id, VkSettings.login, VkSettings.password, VkSettings.chat_id)
ai.work()