from enum import Enum, auto


class ReadingKind(Enum):
    """ Enum describing what kind of values event returns"""
    SENSOR_SPECIFIC = auto()
    THRESHOLD = auto()
    DISCRETE = auto()
    UNSUPPORTED = auto()


DISCRETE_READING_RANGE = list(range(0x02, 0xD))
SENSOR_SPECIFIC_READING_CODE = 0x6F
THRESHOLD_READING_CODE = 0x01


def get_reading_kind(reading_code):
    "Returns event reading kind based on given sensor code"
    mapped_kind = {
        THRESHOLD_READING_CODE: ReadingKind.THRESHOLD,
        SENSOR_SPECIFIC_READING_CODE: ReadingKind.SENSOR_SPECIFIC,
    }.get(reading_code)
    if isinstance(mapped_kind, ReadingKind):
        return mapped_kind
    if reading_code in DISCRETE_READING_RANGE:
        return ReadingKind.DISCRETE
    return ReadingKind.UNSUPPORTED


def get_reading_kind_readable(kind: ReadingKind) -> str:
    "Returns readable sensor's reading kind"
    return {
        ReadingKind.SENSOR_SPECIFIC: 'sensor_specific',
        ReadingKind.THRESHOLD: 'threshold',
        ReadingKind.DISCRETE: 'discrete',
        ReadingKind.UNSUPPORTED: 'unsupported',
    }[kind]
