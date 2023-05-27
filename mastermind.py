# SOURCE: https://web.archive.org/web/20140909031305/https://lirias.kuleuven.be/bitstream/123456789/164803/1/kbi_0806.pdf

from collections import Counter
import random

PINS = 4
NUM_COLORS = 6
COLORS = [i + 1 for i in range(NUM_COLORS)]
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

# TODO:
# create a guess object to make guesses more explicit
#   then remove all the copies

class Guess:
    """class for representing guesses"""
    def __init__(self, colors: list[int]):
        if len(list) != PINS:
            raise Exception(f'Invalid colors list. List must contain {PINS} elements')
        for color in colors:
            if color not in range(1, NUM_COLORS+1):
                raise Exception(f'Invalid color in list. Color value must be in range [1, {NUM_COLORS}]')
        self.colors = colors

    def check(self, guess: Guess, answer: Guess) -> tuple:
        """Returns the amount of exact matches and near matches in a tuple

        Args:
            guess (list[str]): the user's guess containing 4 different colors
            answer (list[str]): the randomly generated answer containing 4 different
            colors

        Returns:
            tuple: a tuple (exact_matches, near_matches) where exact matches is when
            the guess and answer list have the exact same color at an index in the
            lists and near matches is the same color is found in both lists but not on
            the same index.
        """
        exact_matches = 0
        near_matches = 0

        for guess_i, answer_i in zip(guess.colors, answer.colors):
            if guess_i == answer_i:
                exact_matches += 1

        guess_count = Counter(guess.colors)
        answer_count = Counter(answer.colors)

        for guess_i in guess_count:
            if guess_i in answer_count:
                near_matches += min(guess_count[guess_i], answer_count[guess_i])

        near_matches -= exact_matches

        return (exact_matches, near_matches)


def probabilty(chance: float) -> bool:
    """Returns boolean based on chance

    Args:
        chance float: some float [0,1] used as a probability that the function
        return true
    Returns:
        bool: the simulated outcome
    """
    return random.random() <= chance


def random_code(population: list[Guess]) -> list[Guess]:
    """Returns a random code that is not already in the population

    Args:
        population: a list of possible guesses/answers
    Returns:
        list: a random guess not already present in the population
    """
    return random.choice([x for x in POSSIBLE_CODES if x not in population])



def crossover(code1: list, code2: list, n: int) -> tuple:
    """
    can't remeber waht this does XD
    """
    c1 = code1.copy()
    c2 = code2.copy()
    crossover_points = random.sample([i for i in range(NUM_COLORS)], k=n)
    for crossover_point in crossover_points:
        c1[crossover_point:], c2[crossover_point:] = (
            c2[crossover_point:],
            c1[crossover_point:],
        )

    return c1, c2


# swaps random color for a different color
def mutation(code: list) -> list:
    c = code.copy()
    idx = random.randint(0, PINS - 1)
    removed = c.pop(idx)
    new_num = random.choice(list(filter(lambda x: x != removed, COLORS))) # remove the lambda
    c.insert(idx, new_num)
    return c


# swapping two random indexes in a chromosome
def permutation(code: Guess) -> Guess:
    c = code.copy()
    idx1, idx2 = random.sample(range(4), k=2)
    c[idx1], c[idx2] = c[idx2], c[idx1]
    return c


# reverses a subset of the chromosome
def inversion(code: Guess) -> Guess:
    c = code.copy()
    start, stop = sorted(random.sample(range(PINS), k=2))
    c[start : stop + 1] = reversed(c[start : stop + 1])
    return c


# fitness function
def fitness(code: list, guesses: list) -> int:
    fitness_score = 0

    fitness_score += sum(
        abs(check(code, guess)[0] - score[0]) + abs(check(code, guess)[1] - score[1])
        for guess, score in guesses
    )

    return fitness_score


def main():
    guesses = []
    population = random.sample(POSSIBLE_CODES, k=150)

    answer = [random.randint(1, len(COLORS)) for _ in range(PINS)]
    guess = [1, 1, 2, 3]  # start with optimal preselected guess
    results = check(guess, answer)  # (correct matches, near matches)
    guesses.append((guess, results))

    # logging information
    print("Answer:", answer)
    print("guess:", guess)
    print(f"exact matches: {results[0]}\nnear matches: {results[1]}")


    while results[0] != PINS:
        eligable_codes = []
        generation = 1

        while generation <= MAX_GEN and len(eligable_codes) <= MAX_SIZE:
            # create a new population
            new_pop = []
            for _ in range(75):
                code1, code2 = random.choices(population, k=2)
                code1, code2 = crossover(code1, code2, random.randint(1, 2))

                if code1 not in new_pop:
                    new_pop.append(code1)
                else:
                    new_pop.append(random_code(population=new_pop))

                if code2 not in new_pop:
                    new_pop.append(code2)
                else:
                    new_pop.append(random_code(population=new_pop))

            population = new_pop

            # further randomization of the codes
            for idx, code in enumerate(population):
                if probabilty(0.03):
                    population[idx] = permutation(code)

                if probabilty(0.03):
                    population[idx] = mutation(code)

                if probabilty(0.02):
                    population[idx] = inversion(code)

            # run fitness function on the codes finding eligable chromosomes
            for code in population:
                if (
                    fitness(code=code, guesses=guesses) == 0
                    and code not in eligable_codes
                ):
                    eligable_codes.append(code)

            generation += 1

        # new population should consist of only parents from the last eligable set
        population = eligable_codes.copy()
        guess = random.choice(eligable_codes)
        results = check(guess, answer)
        guesses.append((guess, results))

        print("guess:", guess)
        print(f"exact matches: {results[0]}\nnear matches: {results[1]}")


if __name__ == "__main__":
    main()
