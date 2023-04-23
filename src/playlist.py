import datetime
import isodate

from src.channel import ABCYoutube


class PlayList(ABCYoutube):
    """
    Класс для представления плейлиста
    """

    def __init__(self, playlist_id: str):
        self.playlist_id = playlist_id
        self.playlist_info = self.get_service().playlists().list(id=playlist_id,
                                                                 part='snippet, contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()

        self.title = self.playlist_info['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_id

        self.__playlist_videos = self.get_service().playlistItems().list(playlistId=playlist_id,
                                                                         part='contentDetails',
                                                                         maxResults=50,
                                                                         ).execute()

        self.__video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]
        self.__video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                                 id=','.join(self.__video_ids)
                                                                 ).execute()

    @property
    def total_duration(self) -> datetime.timedelta:
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста.
        """
        total = datetime.timedelta()

        for video in self.__video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration

        return total

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).
        """
        best_video = ''
        max_like = 0

        for video in self.__video_response['items']:
            like_count = int(video['statistics']['likeCount'])

            if like_count > max_like:
                max_like = like_count
                best_video = video['id']

        return 'https://youtu.be/' + best_video
