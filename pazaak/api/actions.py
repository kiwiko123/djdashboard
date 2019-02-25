import enum


class Actions(enum.Enum):
    END_TURN_PLAYER = 'end-turn-player'
    END_TURN_OPPONENT = 'end-turn-opponent'
    HAND_PLAYER = 'hand-player'
    STAND_PLAYER = 'stand-player'
