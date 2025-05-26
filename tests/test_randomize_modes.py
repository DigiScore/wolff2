from modules.randomize_modes import generate_random_modes


def test_randomize_modes():
    for _ in range(10):
        modes = generate_random_modes()
        ones = modes.count(1)
        zeros = modes.count(0)
        assert ones == zeros
