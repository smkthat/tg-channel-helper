import os
import yaml
import dotenv

from dataclasses import dataclass

from app.configuration.log import get_logger
from app.halpers.decorators import singleton

LOGGER = get_logger(__name__, '../../logs')

BOT_TOKEN_FORMAT = 'BOT_{}'


@singleton
class Config:
    """This class is used for configuration of application.
    It is a singleton, so that it can be shared across the application.

    Attributes:
        __ENCODING: Used to set the encoding of the file.
        CONFIG_PATH: Path of the default configuration file.
    """
    __ENCODING = 'utf-8'
    CONFIG_PATH = os.path.relpath('default.yaml')

    @dataclass
    class App:
        debug: bool

        def __init__(self, debug: bool = False) -> None:
            self.debug = debug

    @dataclass
    class Bot:
        id: int
        enabled: bool
        owner_id: int
        channel_id: int
        admin_chat: dict

        @property
        def admin_chat_id(self) -> int:
            return self.admin_chat.get('chat_id')

        @property
        def thread_id(self) -> int:
            return self.admin_chat.get('thread_id')

        def __init__(self, id: int, enabled: bool, owner_id: int, channel_id: int, admin_chat: dict) -> None:
            self.id = id
            self.enabled = enabled
            self.owner_id = owner_id
            self.channel_id = channel_id
            self.admin_chat = admin_chat

    @dataclass
    class Redis:
        host: str
        port: int
        db: int

        def __init__(self, db: int, host: str = '127.0.0.1', port: int = 6379) -> None:
            self.db = db
            self.host = host
            self.port = port

    __app: App
    __bots: dict[str, Bot]
    __redis: Redis

    def __init__(self):
        LOGGER.debug('load configuration')
        config_data = self.read_yaml(file_path=self.CONFIG_PATH)
        self.__app = self.App(
            debug=config_data['App']['debug']
        )
        self.__bots = {
            bot['id']: self.Bot(
                id=bot['id'],
                enabled=bot['enabled'],
                owner_id=bot['owner_id'],
                channel_id=bot['channel_id'],
                admin_chat=bot['admin_chat'],
            ) for bot in config_data['Bots']
        }
        self.__redis = self.Redis(
            db=config_data['Redis']['db'],
            host=config_data['Redis']['host'],
            port=config_data['Redis']['port']
        )

    @property
    def app(self) -> App:
        return self.__app

    @property
    def bots(self) -> dict[str, Bot]:
        return self.__bots

    @property
    def redis(self) -> Redis:
        return self.__redis

    @classmethod
    def read_yaml(cls, file_path: str) -> dict:
        """Used to read the data from the given configuration file."""
        file_path = os.path.relpath(file_path)
        LOGGER.debug(f'read configuration file "{file_path}"')
        if os.path.isfile(file_path):
            with open(file_path, mode="r", encoding=cls.__ENCODING) as file:
                try:
                    return yaml.safe_load(file)
                except yaml.YAMLError as e:
                    LOGGER.error(e)
        else:
            LOGGER.fatal(f'Please, provide "{file_path}" file.')
            exit(f'Missing file "{file_path}".')

    @classmethod
    def dump_config(cls, file_path: str, data: object):
        """Used to dump the configuration data to the given configuration file."""
        LOGGER.debug(f'dump configuration file "{file_path}')
        with open(file_path, mode='w', encoding=cls.__ENCODING) as file:
            yaml.safe_dump(
                data=data.__dict__,
                stream=file,
                sort_keys=False,
                allow_unicode=True,
                encoding=cls.__ENCODING,
                default_flow_style=False
            )


def check_bot_token(bot_id: int) -> bool:
    """
    Validates the existence and non-emptiness of a bot token environment variable for a given bot ID.
    
    :param bot_id: Integer representing the bot identifier
    :return: True if the token exists and is non-empty, raises RuntimeError otherwise
    """
    env_vars = dotenv.dotenv_values()
    required_var = BOT_TOKEN_FORMAT.format(bot_id)
    
    if required_var not in env_vars or not env_vars[required_var]:
        raise RuntimeError(f'Please, provide {required_var} variable in .env file. See example on .env.template')
    
    return True


dotenv.load_dotenv()
CONFIG = Config()
