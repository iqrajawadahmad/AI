import random

# Get user input for the target sequence and initial binary string
print("GENETIC ALGORITHM FOR BINARY STRING MATCHING")
print("Problem Solved: Evolving a population of binary strings to match a specific target sequence.")
TARGET_SEQUENCE = input("Enter the target binary sequence (e.g., 10101010): ")
initial_string = input("Enter the initial binary string (must be same length as target): ")
POPULATION_SIZE = 5  # Fixed population size
CROSSOVER_RATE = 0.9  # Crossover probability
MUTATION_RATE = 0.01  # Mutation probability
NUM_GENERATIONS = 50
GENES = ["0", "1"]

# Ensure initial string matches target length
if len(initial_string) != len(TARGET_SEQUENCE):
    raise ValueError("Initial binary string must be the same length as the target sequence.")

# Fitness function: Calculates number of matching bits with the target
def fitness(chromosome):
    return sum(1 for i in range(len(TARGET_SEQUENCE)) if chromosome[i] == TARGET_SEQUENCE[i])

# Generate a random chromosome
def create_individual():
    return ''.join(random.choice(GENES) for _ in range(len(TARGET_SEQUENCE)))

# Generate initial population with the given initial string and random strings
def initialize_population():
    population = [initial_string]  # Start with user-defined initial string
    for _ in range(POPULATION_SIZE - 1):
        population.append(create_individual())
    return population

# Selects the two fittest individuals as parents
def selection(population):
    return sorted(population, key=fitness, reverse=True)[:2]

# Crossover: Combines two parents to create two offspring
def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:  # Apply crossover based on probability
        crossover_point = random.randint(1, len(TARGET_SEQUENCE) - 1)
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        offspring1, offspring2 = parent1, parent2  # No crossover; offspring are clones of parents
    return offspring1, offspring2

# Mutation: Randomly flips bits in the chromosome
def mutate(chromosome):
    chromosome = list(chromosome)
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:  # Apply mutation based on probability
            chromosome[i] = '1' if chromosome[i] == '0' else '0'
    return ''.join(chromosome)

# Run the genetic algorithm
population = initialize_population()  # Initialize with user-defined initial string

for generation in range(NUM_GENERATIONS):
    if generation == 0:
        print(f"\nGeneration {generation}  \nInitial Population:")
    else:
        print(f"\nGeneration {generation}  \nNew Population:")

    # Print each chromosome in the new population with its fitness and fitness ratio
    max_fitness = len(TARGET_SEQUENCE)
    for ind in population:
        chrom_fitness = fitness(ind)
        fitness_ratio = (chrom_fitness / max_fitness) * 100  # Calculate fitness ratio as percentage
        print(f"Chromosome: {ind} | Fitness: {chrom_fitness} | Fitness Ratio: {fitness_ratio:.2f}%")

    # Select the best parents for crossover
    parent1, parent2 = selection(population)
    print(f"\nSelected Best Parents:")
    print(f"Parent 1: {parent1} | Fitness: {fitness(parent1)}")
    print(f"Parent 2: {parent2} | Fitness: {fitness(parent2)}")
    print("Applying crossover...")

    # Apply crossover and mutation to generate offspring
    new_population = []
    crossover_offspring = []
    mutation_offspring = []

    while len(new_population) < POPULATION_SIZE:
        # Perform crossover and create two offspring
        offspring1, offspring2 = crossover(parent1, parent2)
        crossover_offspring.extend([offspring1, offspring2])

        # Apply mutation to both offspring
        mutated_offspring1 = mutate(offspring1)
        mutated_offspring2 = mutate(offspring2)
        mutation_offspring.extend([mutated_offspring1, mutated_offspring2])

        # Add both mutated offspring to the new population
        if len(new_population) < POPULATION_SIZE:
            new_population.append(mutated_offspring1)
        if len(new_population) < POPULATION_SIZE:
            new_population.append(mutated_offspring2)

    # Print the offspring after crossover and mutation
    print(f"\nOffspring after crossover:")
    for off in crossover_offspring:
        print(f"Crossover offspring: {off}")

    print(f"\nOffspring after mutation:")
    for off in mutation_offspring:
        print(f"Mutated offspring: {off}")

    # Update the population to the new mutated population
    population = new_population

    # Check if the target sequence is in the new population, and stop if found
    if any(fitness(chrom) == len(TARGET_SEQUENCE) for chrom in population):
        print("\nTarget sequence reached!")
        break  # Stop if target is achieved

    # Print transition to next generation (only if target not achieved)
    if generation < NUM_GENERATIONS - 1:
        print(f"\nPassing to Generation {generation + 1}")
