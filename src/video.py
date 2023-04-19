from src.channel import Channel


class Video(Channel):
    """
    Класс для получения информации о видео
    """
    YT_VIDEO_URL = 'https://www.youtube.com/watch?v='

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=video_id
                                                               ).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.video_url = self.YT_VIDEO_URL + self.video_id
        self.video_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self) -> str:
        """
        Переопределение метода __str__ от класса Channel
        """
        return f'{self.video_title}'


class PLVideo(Video):
    """
    Класс, который инициализируется 'id видео' и 'id плейлиста'
    """
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                       part='contentDetails',
                                                                       maxResults=50,
                                                                       ).execute()
