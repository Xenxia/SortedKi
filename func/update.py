import requests

from logger import Logger

class Update():
    log: Logger
    version: str
    __URL: str = "https://github.com/Xenxia/Tree/releases/latest"

    def __init__(self, log: Logger) -> None:
        self.log = log
        self.version = self.get_response()

    def get_version(self) -> str:
        return self.version

    def get_response(self) -> str:
        self.log.info("Get Version")
        response = requests.get(self.__URL)
        if str(response.status_code) == "404":
            return None
        else:
            return response.url.rsplit('/', 1)[-1]
