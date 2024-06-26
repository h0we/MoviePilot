from datetime import datetime
from functools import lru_cache

import requests

from app.utils.http import RequestUtils


class BangumiApi(object):
    """
    https://bangumi.github.io/api/
    """

    _urls = {
        "calendar": "calendar",
        "detail": "v0/subjects/%s",
        "persons": "v0/subjects/%s/persons",
        "subjects": "v0/subjects/%s/subjects"
    }
    _base_url = "https://api.bgm.tv/"
    _req = RequestUtils(session=requests.Session())

    def __init__(self):
        pass

    @classmethod
    @lru_cache(maxsize=128)
    def __invoke(cls, url, **kwargs):
        req_url = cls._base_url + url
        params = {}
        if kwargs:
            params.update(kwargs)
        resp = cls._req.get_res(url=req_url, params=params)
        try:
            return resp.json() if resp else None
        except Exception as e:
            print(e)
            return None

    def calendar(self, page: int = 1, count: int = 30):
        """
        获取每日放送，返回items
        """
        """
        [
          {
            "weekday": {
              "en": "Mon",
              "cn": "星期一",
              "ja": "月耀日",
              "id": 1
            },
            "items": [
              {
                "id": 350235,
                "url": "http://bgm.tv/subject/350235",
                "type": 2,
                "name": "月が導く異世界道中 第二幕",
                "name_cn": "月光下的异世界之旅 第二幕",
                "summary": "",
                "air_date": "2024-01-08",
                "air_weekday": 1,
                "rating": {
                  "total": 257,
                  "count": {
                    "1": 1,
                    "2": 1,
                    "3": 4,
                    "4": 15,
                    "5": 51,
                    "6": 111,
                    "7": 49,
                    "8": 13,
                    "9": 5,
                    "10": 7
                  },
                  "score": 6.1
                },
                "rank": 6125,
                "images": {
                  "large": "http://lain.bgm.tv/pic/cover/l/3c/a5/350235_A0USf.jpg",
                  "common": "http://lain.bgm.tv/pic/cover/c/3c/a5/350235_A0USf.jpg",
                  "medium": "http://lain.bgm.tv/pic/cover/m/3c/a5/350235_A0USf.jpg",
                  "small": "http://lain.bgm.tv/pic/cover/s/3c/a5/350235_A0USf.jpg",
                  "grid": "http://lain.bgm.tv/pic/cover/g/3c/a5/350235_A0USf.jpg"
                },
                "collection": {
                  "doing": 920
                }
              },
              {
                "id": 358561,
                "url": "http://bgm.tv/subject/358561",
                "type": 2,
                "name": "大宇宙时代",
                "name_cn": "大宇宙时代",
                "summary": "",
                "air_date": "2024-01-22",
                "air_weekday": 1,
                "rating": {
                  "total": 2,
                  "count": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0,
                    "5": 1,
                    "6": 1,
                    "7": 0,
                    "8": 0,
                    "9": 0,
                    "10": 0
                  },
                  "score": 5.5
                },
                "images": {
                  "large": "http://lain.bgm.tv/pic/cover/l/71/66/358561_UzsLu.jpg",
                  "common": "http://lain.bgm.tv/pic/cover/c/71/66/358561_UzsLu.jpg",
                  "medium": "http://lain.bgm.tv/pic/cover/m/71/66/358561_UzsLu.jpg",
                  "small": "http://lain.bgm.tv/pic/cover/s/71/66/358561_UzsLu.jpg",
                  "grid": "http://lain.bgm.tv/pic/cover/g/71/66/358561_UzsLu.jpg"
                },
                "collection": {
                  "doing": 9
                }
              }
            ]
          }
        ]
        """
        ret_list = []
        result = self.__invoke(self._urls["calendar"], _ts=datetime.strftime(datetime.now(), '%Y%m%d'))
        if result:
            for item in result:
                ret_list.extend(item.get("items") or [])
        return ret_list[(page - 1) * count: page * count]

    def detail(self, bid: int):
        """
        获取番剧详情
        """
        return self.__invoke(self._urls["detail"] % bid, _ts=datetime.strftime(datetime.now(), '%Y%m%d'))

    def persons(self, bid: int):
        """
        获取番剧人物
        """
        return self.__invoke(self._urls["persons"] % bid, _ts=datetime.strftime(datetime.now(), '%Y%m%d'))

    def subjects(self, bid: int):
        """
        获取关联条目信息
        """
        return self.__invoke(self._urls["subjects"] % bid, _ts=datetime.strftime(datetime.now(), '%Y%m%d'))
