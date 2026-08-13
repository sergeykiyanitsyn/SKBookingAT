from enum import StrEnum, IntEnum


class Users(StrEnum):
    USERNAME = 'admin'
    PASSWORD = 'password123'

class Timeouts(IntEnum):
    TIMEOUT = 5