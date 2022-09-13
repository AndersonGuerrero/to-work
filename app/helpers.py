import enum
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class CurrencyEnum(str, enum.Enum):
    USD = 'USD'
    COP = 'COP'
