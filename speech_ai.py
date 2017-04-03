import sys
import ChatAI


def greeting():
    print('**********************************')
    print('* Welcome to Speech AI chat-bot! *')
    print('**********************************')

def main():

    # Обработка аргументов командной строки
    if len(sys.argv) == 2 and sys.argv[1] == '-speech':  
        greeting()
        print('Speech mode\n\n')
        ai = ChatAI.ChatAI_Speech()

    elif len(sys.argv) == 2 and sys.argv[1] == '-text':
        greeting()
        print('Text mode\n\n')
        ai = ChatAI.ChatAI_Text()

    else:
        greeting()    
        print('Usage: python speech_ai.py -speech|-text')
        print('Mode:')
        print('  -speech - voice recognition and text-to-speech')
        print('  -text   - text chat in console')
        exit()

    ai.work()
    

main()