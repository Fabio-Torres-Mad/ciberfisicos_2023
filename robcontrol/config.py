from pydantic import BaseModel, Field

class MotorChannel(BaseModel):
    ENA: int
    IN0: int
    IN1: int

class MotorConfig(BaseModel):
    m_right: MotorChannel
    m_left: MotorChannel


class UltrasoundConfig(BaseModel):
    trigger: int
    echo: int


class ServoConfig(BaseModel):
    control: int

DEFAULT_CONF: dict = {
    "motor": {
        "m_right": {
            "ENA": 38,
            "IN0": 35,
            "IN1": 0
        },
        "m_left": {
            "ENA": 40,
            "IN0": 37,
            "IN1": 0
        }
    },
    "servo": {
        "control": 0
    },
    "ultrasound": {
        "trigger": 88,
        "echo": 86
    }
}