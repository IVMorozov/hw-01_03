from api import API_KEY
from typing import Any
import base64
from mistralai import Mistral

class  TextRequest:
    """
    класс для отправки текстовых запросов
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = Mistral(api_key=api_key)
        pass
    def send(self, text: str, model: str, history: list = None) -> dict:
        """
        метод для отправки текстовых запросов, включая историю
        """
        self.text = text
        self.model = model     
        self.client = Mistral(api_key=self.api_key)

        messages = []
        if history:
            messages.extend([{'role': msg['role'], 'content': msg['content']} for msg in history])
        messages.append({'role':'user', 'content': text})
        chat_response = self.client.chat.complete(model = model, messages = messages)
        result = {'role': 'assistant', 'content': chat_response.choices[0].message.content}
        return result

class  ImageRequest:
    """
    класс для отправки запросов с изображением
    """
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = Mistral(api_key=api_key)

    def __encode_image(self, image_path: str) -> str:
        """
        переврд изображения в формат base64
        """
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Ошибка: файл {image_path} не найден.")
            return ""
        except Exception as e:  # Added general exception handling
            print(f"Error: {e}")
            return ""
    
    
    def send(self, text: str, image_path: str, model: str, history: list = None) -> dict:
        """
        метод для отправки текстового запроса совместно с изображением, включая историю
        """
        base64_image = self.__encode_image(image_path)
        messages = []
        if history:
            messages.extend([{'role': msg['role'], 'content': msg['content']} for msg in history])        
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text
                },          
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        } )        

        # Get the chat response
        chat_response = self.client.chat.complete(model=model, messages=messages)

        # Print the content of the response
        result = {'role': 'assistant', 'content': chat_response.choices[0].message.content}
        return result   

        

class  ChatFacade: 
    """
    класс-фасад для объединения функционала и удобного взаимодействия пользователя с системой, управляетвыбором вида взаимодействия с Мистраль (TextRequest|ImageRequest)
    """   
    def __init__(self, api_key: str) -> None: 
        self.api_key = api_key
        self.models: dict[str, list[str]] = {'text':["mistral-large-latest"], 'image':["pixtral-12b-2409"]}
        self.request: TextRequest|ImageRequest = self.__set_request()
        self.model: str = self.__set_model()
        self.history:list[Any]= []

    def __set_request(self) -> TextRequest|ImageRequest:
        """
        метод обеспечивает нициализацию с API-ключом. Создаются экземпляры `TextRequest` и `ImageRequest`
        """
        pass
        
    def __set_model(self) -> str: 
        """
        метод инициализирует список доступных моделей
        """
        if self.mode == '1':
            model:str = "mistral-large-latest"
        
        if self.mode == '2':
            model:str = "pixtral-12b-2409"        
        return model
        

    def ask_question(self, text: str, image_path: str = None) -> dict:
        """
        метод для отправки запроса
        """
        pass
    
    def __call__(self):
        """
        запуск фасада
        -для экономии времени при тестировании ввод заменен подстановкой текста запроса и адреса картинки. Для ручного ввода закоментить строки 146, 150, 151, разкоментить строки 145, 149
        ключ API размещен в файле api.py в этой же директории
        """
        # text:str = input('\n Введите текст запроса')
        pass