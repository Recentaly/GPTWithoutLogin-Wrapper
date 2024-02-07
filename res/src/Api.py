import requests
from typing import Dict, List, Any
from fake_useragent import UserAgent
from secrets import randbelow

class API(object):

    def __init__(self):
        self.url = "https://gptwithoutlogin.com/wp-content/themes/generatepress/api-proxy.php"

        self.__headers = {
                "POST": "/wp-content/themes/generatepress/api-proxy.php HTTP/3",
                "Host": "gptwithoutlogin.com",
                "User-Agent": f"{UserAgent().random}",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://gptwithoutlogin.com/",
                "Content-Type": "application/json",
                "Content-Length": f"{randbelow(100)}",
                "Origin": "https://gptwithoutlogin.com",
                "Alt-Used": "gptwithoutlogin.com",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "TE": "trailers"
            }

    def chat(self, messages: List[Dict[str, str]], model: str, config: Dict[str, Any]):

        __stream = config.get("stream", False)

        data = {
            "frequency_penalty": config.get("frequency_penalty", 0.0),
            "max_tokens": config.get("max_tokens", 150),
            "messages": messages,
            "model": model,
            "n": 1,
            "presence_penalty": config.get("presence_penalty", 0.0),
            "stream": __stream,
            "temperature": config.get("temperature", 0.7),
            "top_p": config.get("top_p", 0.7),
        }

        response = requests.post(self.url, json=data, headers=self.__headers, stream=__stream)
        response.raise_for_status()

        if __stream:
            
            for chunk in response.iter_lines():
                yield chunk

        else:   
            
            try:
                
                yield response.json()
            
            except Exception as e:
                yield response.content.decode("utf-8")
