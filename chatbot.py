import sys
import speech_recognition as sr
import os
import requests
from wit import Wit



WIT_TOKEN = 'DGH7KYZGRV5ZZMEAJQOIGJUXHYYSPKAF'
client = Wit(WIT_TOKEN)
username = input('Xin nhập tên của bạn : ')
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Xin mời nói: ')
        audio = recognizer.listen(source)
        
    try:
       
        text = recognizer.recognize_google(audio, language = 'vi-VN')
        print('Bạn đã nói : ' + text)
        return text
    except sr.UnknownValueError:
        print('Xin lỗi, tôi không thể hiểu ')
        return None
    except sr.RequestError as e:
        print(f'Không thể hiểu yêu cầu dịch vụ google {e}')
        return None
    


def msg_to_wit(text):
    msg_url = f'https://api.wit.ai/message?v=20240304&q={text}'
    headers = {
        'Authorization' : f'Bearer {WIT_TOKEN}'
    }
    response = requests.get(msg_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f'Lỗi khi gửi yêu cầu {response.status_code}')
        return None

def process_wit_response(response):
    if response:
        intents = response.get('intents', [])
        if intents:
            intents_name = intents[0]['name']
            return intents_name
    return "unknow"

def handle_intent(intent):
    if intent == "open_youtube":
        print('Mở youtube bằng chrome')
        os.system('start chrome https://www.youtube.com')
    elif intent == "open_chrome":
        print('Mở chrome')
        os.system("start chrome https://www.google.com")
    elif intent == "byebye":
        print('Hẹn gặp lại...')
        sys.exit(0)
    elif intent == "hello":
        print('Chào bạn : ' + username)
    else:
        print('Intent không nhận diện được')

def main():
    while True:
        print('Đang lắng nghe : ...')
        command = recognize_speech()
       
        
        if command:
            
            wit_response = msg_to_wit(command)
            intent = process_wit_response(wit_response)
            print(f'Intent nhận diện {intent}')
            handle_intent(intent)
            

if __name__ == "__main__":
    main()
