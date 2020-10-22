from poem import Poem
import random
from text_to_speech import read_text_doc


def get_starter_recipes():
    """
    Creates a database of all the starting poems whose urls are listed in the ./urls file.

    :return: An array consisting of all the poems in the starting population.
    """

    poem_list = []  # A list of the various starting best poems

    file = open("./urls")

    for line in file:
        p = Poem(str(line))
        poem_list += p

    return poem_list


def poem_select(poems):
    """
    Pseudo-randomly elects a poem using the poems fitness as the weight.

    :param poems: A list containing all the poems in the current poem database.
    :return: The selected poem
    """

    fitness_list = [poem.fitness() for poem in poems]
    return random.choices(poems, weights=fitness_list)[0]


def poem_characteristics(poem_1, poem_2):

    poem_format = ""  # A template for the result poem to follow


    return poem_format


def main():

    starter_poems = get_starter_recipes()  # All the starter poems as an array

    read_text_doc()


if __name__ == '__main__':
    main()
