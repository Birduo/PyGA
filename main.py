# Python Genetic Algorithm
# Individual must guess solution string of length 8
# fitness = sum (uint dist to each char)

# Tournament Mate Selection (population):
# 1. Randomly pick 2^n individuals (inds)
# 2. 1v1, whichever has lower fitness wins
# 3. 2 winners selected for crossbreeding

import random, math

def create_genome(length: int) -> str:
    return "".join([chr(b) for b in random.randbytes(length)])

# this is the inverse of the fitness function
def genome_error(genome: str, solution: str) -> int:
    return sum([abs(ord(genome[i]) - ord(solution[i])) for i in range(len(genome))])

# performing mutation randomly on genes of a population
# mutation type: complete genome recreation
def mutate_pop_complete(population: list[str], mutation_rate: float) -> list[str]:
    mutation_count = 0

    for i in range(len(population)):
        if random.random() < mutation_rate:
            mutation_count += 1
            population[i] = create_genome(len(population[i]))

    return population

# performing mutation randomly on genes of a population
# mutation type: randomly change one character
def mutate_pop_char(population: list[str], mutation_rate: float) -> list[str]:
    mutation_count = 0

    for i in range(len(population)):
        if random.random() < mutation_rate:
            mutation_count += 1

            out = list(population[i])
            index = random.randrange(0, len(out))
            out[index] = "".join([chr(b) for b in random.randbytes(1)])

            population[i] = "".join(out)
            
    return population

# performing mutation randomly on genes of a population
# mutation type: randomly scramble all characters using random.sample
def mutate_pop_scramble(population: list[str], mutation_rate: float) -> list[str]:
    mutation_count = 0

    for i in range(len(population)):
        if random.random() < mutation_rate:
            mutation_count += 1
            
            out = list(population[i])

            population[i] = "".join(random.sample(out, k=len(out)))

    return population

# input: 2 genomes
# output: crossbreed of 2 genomes into 1
def crossbreed(ga: str, gb: str) -> str:
    out = list(ga)

    # sample some indices to yoink from gb
    for i in random.sample(range(len(gb)), int(len(gb) / 2)):
        out[i] = gb[i]

    return "".join(out)

# input: population, stages (2^stages inds will compete)
# output: winning parents
# note: when implementing, just search for winning genome in list and rem...
# the first instance of it, shouldn't matter which as they're still the winning genome
def tournament_selection(population: list[str], size: int, solution: str) -> str:
    sampled = random.sample(population, size)

    sampled.sort(key=lambda ind: genome_error(ind, solution))

    return sampled[:2]

def main():
    # population size to be sustained throughout simulation
    POP_MAX = 10000
    # max amount of generations (if solution is found program will halt``)
    GEN_MAX = 100
    SOLUTION = "Hello world!"
    # elitism is % of inds that automatically move on
    ELITISM = .1
    # mutation is % chance that an ind gets mutated completely
    MUTATION = .1
    # tourney size is how many inds are selected to compete
    TOURNEY_SIZE = 64

    elitism_count = math.floor(ELITISM * POP_MAX)

    population = [create_genome(len(SOLUTION)) for ind in range(POP_MAX)]

    solution_found = False

    # this is where the evolution happens <3
    for gen in range(GEN_MAX):
        # sort population by best to worst
        population.sort(key=lambda ind: genome_error(ind, SOLUTION))
        print(f"Best scorer for gen {gen}: {population[0]} ({genome_error(population[0], SOLUTION)})")

        if population[0] == SOLUTION:
            solution_found = True
            break

        # make (ELITISM) of the population move on to the next generation
        next_gen = [population[i] for i in range(elitism_count)]
        population = population[elitism_count:]

        for i in range(POP_MAX - elitism_count):
            parents = tournament_selection(population, TOURNEY_SIZE, SOLUTION)
            child = crossbreed(parents[0], parents[1])

            next_gen.append(child)

        # these can be commented out as needed, but its fun to combine them
        population = mutate_pop_complete(next_gen, MUTATION)
        population = mutate_pop_char(next_gen, MUTATION)
        population = mutate_pop_scramble(next_gen, MUTATION)

    if solution_found:
        print("Solution found!")
    else:
        population.sort(key=lambda ind: genome_error(ind, SOLUTION))
        print(f"Best scorer for gen {GEN_MAX}: {population[0]} ({genome_error(population[0], SOLUTION)})")

if __name__ == "__main__":
    main()
