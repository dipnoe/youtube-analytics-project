import os
import json

from googleapiclient.discovery import build


class Channel:
    """
    Класс для ютуб-канала
    """

    API_KEY: str = os.getenv('YT_API_KEY')
    YT_URL: str = 'https://www.youtube.com/channel/'

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        """
        youtube = build('youtube', 'v3', developerKey=cls.API_KEY)
        return youtube

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API
        """
        self.__channel_id = channel_id

        self.channel_info = self.get_service().channels(). \
            list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.url = self.YT_URL + self.__channel_id
        self.subscriber_count = int(self.channel_info['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel_info['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.channel_info['items'][0]['statistics']['viewCount'])

    def __str__(self) -> str:
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        """
        Сложение количества подписчиков двух каналов
        """
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other) -> int:
        """
        Вычитание количества подписчиков двух каналов
        """
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other) -> bool:
        """
        Сравнение «меньше» количество подписчиков двух каналов
        """
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other) -> bool:
        """
        Сравнение «меньше или равно» количество подписчиков двух каналов
        """
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other) -> bool:
        """
        Сравнение «больше» количество подписчиков двух каналов
        """
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other) -> bool:
        """
        Сравнение «больше или равно» количество подписчиков двух каналов
        """
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other) -> bool:
        """
        Сравнение «равно» количество подписчиков двух каналов
        """
        return self.subscriber_count == other.subscriber_count

    @property
    def channel_id(self):
        """
        Геттер для channel_id
        """
        return self.__channel_id

    @staticmethod
    def print_json(dict_to_print) -> None:
        """
        Выводит словарь json
        """
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self) -> None:
        """
        Выводит в консоль информацию о канале
        """
        channel = self.get_service().channels(). \
            list(id=self.channel_id, part='snippet,statistics').execute()
        self.print_json(channel)

    @property
    def data(self) -> dict:
        """
        Геттер для data
        """
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        return data

    def to_json(self, file) -> None:
        """
        Метод to_json(), сохраняющий в файл значения атрибутов экземпляра Channel
        """
        with open(file, 'a') as f:

            if os.stat(file).st_size == 0:
                json.dump([self.data], f)

            else:

                with open(file) as json_file:
                    data_list = json.load(json_file)
                data_list.append(self.data)

                with open(file, "w") as json_file:
                    json.dump(data_list, json_file)
