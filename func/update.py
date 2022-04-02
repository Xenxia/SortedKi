import requests
from logger import Logger

class Update():
    log: Logger
    version: str
    __URL: str = "https://github.com/Xenxia/SortedTree/releases/latest"

    def __init__(self, log: Logger) -> None:
        self.log = log
        self.version = self.get_response()

    def get_version(self) -> str:
        return self.version

    def get_response(self) -> str:
        self.log.info("Get Version")
        try:
            response = requests.get(self.__URL, timeout=2)
            return response.url.rsplit('/', 1)[-1]

        except requests.exceptions.HTTPError:
            self.log.error("HTTPerror")

        except requests.exceptions.Timeout:
            self.log.error("TimeOut")

        except requests.exceptions.TooManyRedirects:
            self.log.error("TooManyRedirects")

        except requests.exceptions.ConnectionError:
            self.log.error("ConnectionError")

        except requests.exceptions.RequestException:
            self.log.error("RequestException")

        return "none"
            
