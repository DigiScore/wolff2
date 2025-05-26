import random
from typing import List


def generate_random_modes() -> List[int]:
    random_list = []
    for _ in range(3):
        first_number = random.randint(0, 1)
        random_list.append(first_number)
        if first_number == 1:
            random_list.append(0)
        else:
            random_list.append(1)
    return random_list
