# SOURCE: https://web.archive.org/web/20140909031305/https://lirias.kuleuven.be/bitstream/123456789/164803/1/kbi_0806.pdf

import random
from collections import Counter

# general game variables
PINS = 4
COLORS = [i + 1 for i in range(6)]
NUM_COLORS = len(COLORS)
POSSIBLE_CODES = [
    [x, y, z, w]
    for x in range(NUM_COLORS)
    for y in range(NUM_COLORS)
    for z in range(NUM_COLORS)
    for w in range(NUM_COLORS)
]

# algorithm parameters
MAX_SIZE = 60
MAX_GEN = 100


def check(guess: list, answer: list) -> tuple:
    exact_matches = 0
    near_matches = 0

    # checking for exact matches
    for guess_i, answer_i in zip(guess, answer):
        if guess_i == answer_i:
            exact_matches += 1

    guess_count = Counter(guess)
    answer_count = Counter(answer)

    for guess_i in guess_count:
        if guess_i in answer_count:
            near_matches += min(guess_count[guess_i], answer_count[guess_i])

    near_matches -= exact_matches

    return (exact_matches, near_matches)


# simple RNG function. could be better
def probabilty(chance: float) -> bool:
    if random.random() <= chance:
        return True

    return False


# returns a random combination from the possible choices that isn't already in the population
def random_code(population: list) -> list:
    return random.choice(filter(lambda x: x not in population, POSSIBLE_CODES))


def crossover(code1: list, code2: list, n: int) -> tuple:
    c1 = code1.copy()
    c2 = code2.copy()

    crossover_points = random.choices([i for i in range(0, NUM_COLORS)], k=n)

    for crossover_point in crossover_points:
        c1[crossover_point:], c2[crossover_point:] = (
            c2[crossover_point:],
            c1[crossover_point:],
        )

    return c1, c2


def mutation(code: list) -> list:
    c = code.copy()

    # randomly selected an index
    idx = random.randint(0, PINS - 1)

    # remove element
    removed = c.pop(idx)

    # find a number that is not removed
    new_num = random.choice(list(filter(lambda x: x != removed, COLORS)))

    # insert the new num
    c.insert(idx, new_num)
    return c


def permutation(code: list) -> list:
    c = code.copy()

    # select two random indexes
    idx1, idx2 = random.sample(range(4), k=2)

    # swap the values at either location
    c[idx1], c[idx2] = c[idx2], c[idx1]

    # return the new code
    return c


def inversion(code: list) -> list:
    c = code.copy()


# SHOULDN'T NEED THIS I DON'T THINK
# def diff(tup1, tup2):
#     '''
#     finds the different between two tuples of length 2
#     diff = |tup2 - tup1|
#     '''
#     return (abs(tup2[0]-tup1[0]), abs(tup2[1]-tup1[1]))

# fitness function\
def fitness(code: list, guesses: list) -> int:
    fitness_score = 0

    # finds the sum of differences between the previous guesses and the current guess IF the previous guess was the secret code
    fitness_score += sum(
        abs(check(code, guess)[0] - score[0]) for guess, score in guesses
    )

    # might be able to combine this with the line above it
    fitness_score += sum(
        abs(check(code, guess)[1] - score[1]) for guess, score in guesses
    )

    # wtf does this line even do XDD (we will take it out for now)
    #fitness_score += 2 * PINS * (len(guesses) - 1)
    return fitness_score


def main():
    guesses = []
    i = 1
    population = None

    answer = [random.randint(1, len(COLORS)) for _ in range(PINS)]
    guess = [1, 1, 2, 3]
    results = check(guess, answer)
    guesses.append((guess, results))

    while results[0] != PINS:
        i += 1
        # shouldn't actually be a set most likely a list of lists
        eligable_codes = set()
        h = 1

        while h <= MAX_GEN and len(eligable_codes) <= MAX_SIZE:
            # run the checks in here to see if there are any copies
            for _ in range(75):
                code1, code2 = random.choices(population, k=2)
                code1, code2 = crossover(code1, code2, random.randint(1, 2))

            for idx, code in enumerate(population):
                if probabilty(0.03):
                    population[idx] = mutation(code)

            for idx, code in enumerate(population):
                if probabilty(0.03):
                    population[idx] = permutation(code)

            # fit in the last randomizing function

            # run fitness function on the codes
            for code in population:
                if fitness(code=code, guesses=guesses) == 0:
                    eligable_codes.add(tuple(code))


if __name__ == "__main__":
    main()
