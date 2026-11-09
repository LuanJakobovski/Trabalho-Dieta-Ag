import numpy as np
from numpy import random
from typing import Final, List

class Cromossomo:
    def __init__(self, dieta: List[int]):
        self.DIETA: Final[List[int]] = dieta
        self.SIZE_CROMO: Final[int] = len(self.DIETA)
        self.SIZE_POP: Final[int] = self.SIZE_CROMO * 2

