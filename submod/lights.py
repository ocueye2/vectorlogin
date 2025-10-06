import requests

class HomeAssistantScenes:
    def __init__(self, url: str, token: str):
        """
        :param url: Base URL of Home Assistant (e.g. http://homeassistant.local:8123)
        :param token: Long-lived access token from Home Assistant
        """
        self.url = url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def activate(self, scene_id: str):
        """
        Turn on a scene
        :param scene_id: Scene entity_id (e.g. scene.movie_time)
        """
        endpoint = f"{self.url}/api/services/scene/turn_on"
        data = {"entity_id": scene_id}
        response = requests.post(endpoint, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
