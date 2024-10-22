"""
Задача 6: моделювання еволюції в паралельних середовищах.

Створіть симуляцію еволюції популяції організмів,
де кожен організм обробляється окремо в різних процесах або потоках.

Популяція повинна змінюватися залежно від певних параметрів
(наприклад, харчування, розмноження тощо).
"""

import random
from multiprocessing import Pool


# ---- Define Organism Class and Subclasses ----
class Organism:
    """
    Represent an organism with species, age, and health.

    The Organism class contains logic for aging and survival based on food availability.

    :var species: The species of the organism.
    :type species: str
    :var age: The age of the organism.
    :type age: int
    :var health: The health level of the organism.
    :type health: int
    :var alive: The survival status of the organism.
    :type alive: bool
    """

    def __init__(self, species, age=0, health=100):
        """
        Initialize an Organism instance with species, age, and health.

        :param species: The species of the organism.
        :type species: str
        :param age: The initial age of the organism (default is 0).
        :type age: int
        :param health: The initial health of the organism (default is 100).
        :type health: int
        """
        self.species = species
        self.age = age
        self.health = health
        self.alive = True

    def live_one_year(self, food_factor):
        """
        Simulate one year of life for the organism, including food availability and aging.

        :param food_factor: The probability that food is available in a given year.
        :type food_factor: float
        """
        food_available = random.random() < food_factor
        if food_available:
            self.health += 5
        else:
            self.health -= 15
        self.age += 1
        if self.health <= 0 or self.age >= 15:
            self.alive = False


class Cat(Organism):
    """
    Represent a Cat, inheriting from Organism.
    """

    def __init__(self, age=0, health=100):
        """
        Initialize a Cat instance with age and health.

        :param age: The initial age of the cat.
        :type age: int
        :param health: The initial health of the cat.
        :type health: int
        """
        super().__init__('Cat', age, health)


class Dog(Organism):
    """
    Represent a Dog, inheriting from Organism.
    """

    def __init__(self, age=0, health=100):
        """
        Initialize a Dog instance with age and health.

        :param age: The initial age of the dog.
        :type age: int
        :param health: The initial health of the dog.
        :type health: int
        """
        super().__init__('Dog', age, health)


# ---- Define Simulation Functions ----
def random_event(organism):
    """
    Simulate random events that affect the organism's health, such as disease or natural disasters.

    :param organism: The organism affected by the random event.
    :type organism: Organism
    """
    event_chance = random.random()
    if event_chance < 0.05:
        # 5% chance of disease
        organism.health -= 30
    elif event_chance < 0.10:
        # 5% chance of natural disaster
        organism.health -= 50


def simulate_one_year(organism, food_factor):
    """
    Simulate one year of life for an organism, including aging, food availability, and random events.

    :param organism: The organism whose year is being simulated.
    :type organism: Organism
    :param food_factor: The probability that food is available in a given year.
    :type food_factor: float
    :return: The updated organism after one year.
    :rtype: Organism
    """
    organism.live_one_year(food_factor)
    random_event(organism)
    return organism


# ---- Main Simulation Loop ----
if __name__ == '__main__':
    population = [Cat() for _ in range(10)] + [Dog() for _ in range(15)]
    years = 30
    food_factor = 0.8
    breed_factor = 0.2

    for year in range(1, years + 1):
        print(f"\nYear {year}")
        with Pool() as pool:
            processed_population = pool.starmap(
                simulate_one_year,
                [(organism, food_factor) for organism in population]
            )

        updated_population = [organism for organism in processed_population if organism.alive]

        # Breeding simulation
        offsprings = []
        for organism in updated_population:
            if random.random() < breed_factor:
                if organism.species == 'Cat':
                    offsprings.append(Cat())
                elif organism.species == 'Dog':
                    offsprings.append(Dog())

        population = updated_population + offsprings

        num_cats = sum(1 for organism in population if organism.species == 'Cat')
        num_dogs = sum(1 for organism in population if organism.species == 'Dog')
        print(f"Total population: {len(population)} (Cats: {num_cats}, Dogs: {num_dogs})")
