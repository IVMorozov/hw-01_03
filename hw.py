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
        mode:str = input('Укажите тип запроса: 1 – текстовый, 2 – с изображением: ')
        if mode == '1':
            self.mode = '1'
            return TextRequest(api_key=self.api_key)
        elif mode == '2':
            self.mode = '2'
            return ImageRequest(api_key=self.api_key)
        else:
            raise ValueError("Неверныый режим запроса")
        
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
        user_message = {'role': 'user', 'content': text}
        current_history = [msg for _, msg in self.history]

        if image_path:
            response:dict[Any, Any] = self.request.send(text=text, image_path=image_path, history=current_history, model=self.model)
        else: 
            response:dict[Any, Any] = self.request.send(text=text, history=current_history, model=self.model)
        self.history.append((text, user_message))
        self.history.append((text, response))
        return response
    
    def __call__(self):
        """
        запуск фасада
        -для экономии времени при тестировании ввод заменен подстановкой текста запроса и адреса картинки. Для ручного ввода закоментить строки 146, 150, 151, разкоментить строки 145, 149
        ключ API размещен в файле api.py в этой же директории
        """
        # text:str = input('\n Введите текст запроса')
        text:str = 'расскажи шутку'
        image_path = None
        if isinstance (self.request, ImageRequest):
            # image_path:str = input('ВВедите путь к изображению') 
            text = 'опиши картинку'
            image_path:str = 'lemon.jpg'
        response:dict[Any, Any] = self.ask_question(text=text, image_path=image_path if image_path else None)
        print(response)

chat_facade = ChatFacade(api_key=API_KEY)
chat_facade()