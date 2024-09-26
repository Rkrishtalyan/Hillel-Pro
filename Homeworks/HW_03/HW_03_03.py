"""
3. To-Compare.

1)	Реалізуйте клас Person із параметрами name та age. Додайте методи для порівняння за віком (__lt__, __eq__, __gt__).

2)	Напишіть програму для сортування списку об'єктів класу Person за віком.
"""


class Person:
    """
    Represent a person with a name and age.

    The Person class allows comparison between instances based on age.

    :var name: The name of the person.
    :type name: str
    :var age: The age of the person.
    :type age: int
    """

    def __init__(self, name, age):
        """
        Initialize a Person instance with name and age.

        :param name: The name of the person.
        :type name: str
        :param age: The age of the person.
        :type age: int
        """
        self.name = name
        self.age = age

    def __eq__(self, other):
        """
        Compare equality between two Person instances based on age.

        :param other: Another Person instance to compare with.
        :type other: Person
        :return: True if both persons have the same age, False otherwise.
        :rtype: bool
        :raises TypeError: If the other object is not an instance of Person.
        """
        if isinstance(other, Person):
            return self.age == other.age
        raise TypeError("The other object is not a Person instance")

    def __lt__(self, other):
        """
        Compare if the current Person instance is younger than another Person.

        :param other: Another Person instance to compare with.
        :type other: Person
        :return: True if the current person is younger, False otherwise.
        :rtype: bool
        :raises TypeError: If the other object is not an instance of Person.
        """
        if isinstance(other, Person):
            return self.age < other.age
        raise TypeError("The other object is not a Person instance")

    def __gt__(self, other):
        """
        Compare if the current Person instance is older than another Person.

        :param other: Another Person instance to compare with.
        :type other: Person
        :return: True if the current person is older, False otherwise.
        :rtype: bool
        :raises TypeError: If the other object is not an instance of Person.
        """
        return not self.age < other.age

    def __call__(self):
        """
        Return a dictionary representation of the Person instance.

        :return: A dictionary with the person's name and age.
        :rtype: dict
        """
        return {"name": self.name, "age": self.age}


student_1 = Person('John', 21)
student_2 = Person('Dave', 22)
student_3 = Person('Jane', 19)
teacher = Person('Mr. Twister', 44)

print(f"{student_1.name} is older than {student_2.name}: {student_1 > student_2}")
print(f"{student_1.name} is younger than {student_2.name}: {student_1 < student_2}")
print(f"{student_3.name} is same the age as {teacher.name}: {student_3 == teacher}")

people = []
print(people)

people.extend([student_1(), student_2(), student_3(), teacher()])
print(people)

people = sorted(people, key=lambda person: person["age"])
print(people)
