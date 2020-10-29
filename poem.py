"""
This class functions to read 43 poems listed as the "best poems" by the website
Lit Hub. The class creates an instance of a poem for each poem which includes attributes
for the poem's word frequencies, the rhyme scheme, syllable count, line count, and stanzas.

NOTE: read_poem code was adapted from code developed in a group project with Sam Rousell and Gerard Goucher. The code
was originally written by Sam and the general framework was given by his code. The loop in the function was adapted
from code posted to the public github of Zhiming Wang @zmwangx in his html-to-text repository. This repository was
referenced as a guide for how to use BeautifulSoup to save line separators (stanzas).
"""
import pronouncing as pronouncing
import requests as rq
from bs4 import BeautifulSoup
from nltk.corpus import cmudict


def read_poem(address) -> str:
    """
    Takes in a url and then uses BeautifulSoup to find the poem text on the webpage and then store the poem body.

    :param address: The url of the poem to be stored
    :return: The poem as a string
    """
    p_readable = ""

    site = rq.get(address)

    soup = BeautifulSoup(site.text, 'html.parser')
    title = soup.h1.text

    p_readable += title.strip() + "\n"

    body = soup.find('div', attrs={"class": "c-feature-bd"})

    for line in body.descendants:

        if isinstance(line, str):

            p_readable += line.strip()

        elif line.name == 'br' or line.name == 'p':

            p_readable += '\n'

    poem_as_array = p_readable.split('\n')

    return poem_as_array


def count_stanzas(poem_as_array):
    """
    Counts the number of stanzas in a poem.

    :param poem_as_array: The poem whose stanzas are being counted
    :return:
    """
    count = 0

    for line in poem_as_array:

        if not line.strip():
            count += 1

    return count - 1


def count_lines(poem_as_array):
    """
    Counts the number of lines in a poem (not including the title).

    :param poem_as_array: The poem as a string.
    :return: The number of lines in the poem.
    """

    return len(poem_as_array) - 1


def count_syl(poem_stripped):
    """
    Takes in a poem as string and then counts the number of syllables per line in the poem.

    Note that in English, all syllables have at least one vowel and that consecutive vowels mean count only as a single
    syllable.

    NOTE: This code was adapted in part by code provided on stackoverflow by users @Dawny33 and @The Matt.
    Credit for this code belongs to them. The forum page can be found here:
    https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word

    :param poem_stripped: An array containing only the text-filled lines of the poems
    :return syl_per_line: An array listing the number of syllables per line
    """

    syl_per_line = [-1] * (len(poem_stripped) - 1)

    dic = cmudict.dict()

    i = 0

    while i < len(poem_stripped) - 2:

        current_line = poem_stripped[i]

        c_line_words = current_line.split(" ")

        line_total = 0

        for word in c_line_words:

            try:

                word_total = [len(list(y for y in x if y[-1].isdigit())) for x in dic[word.lower()]][0]

            except KeyError:

                word_total = manual_syl_count(word)

            line_total += word_total

        syl_per_line[i] = line_total

        i += 1

    return syl_per_line


def manual_syl_count(word):
    """
    Manually counts the number of syllables in a given word. This function is only called when a word is not found in
    the cmudict pronunciation library.

    NOTE: This code was adapted for use from a stackoverflow answer posted by user @The Matt.
    All credit for this code belongs to The Matt. The forum page can be found here:
    https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word.

    :param word: The word we want to find the number of syllables in.
    :return: The number of syllables in the given word.
    """

    total = 0

    vowels = "aeiouyAEIOUY"

    if word[0] in vowels:

        total += 1

    i = 1
    while i < len(word):

        if word[i] in vowels and word[i -1] not in vowels:

            total += 1

        i += 1

    if word.endswith('e'):

        total -= 1

    if word.endswith('le'):

        total += 1

    if total == 0:

        total += 1

    return total


def strip_poem_body(poem_as_array):
    """
    Takes in a poem as an array and returns a new array containing only the non-blanks lines of the poem body.

    :param poem_as_array: The poem as an array with title and blank lines.
    :return: A new array with no title or blank lines.
    """

    poem_stripped = []

    i = 1
    while i < len(poem_as_array) - 1:

        if poem_as_array[i].strip():

            poem_stripped.append(poem_as_array[i])

        i += 1

    return poem_stripped


def find_end_rhymes(stripped_body):
    """
    Takes in the poem as an array of strings and then determines the end rhyme pattern.

    The end rhyme pattern is returned as an array where the index of the array value corresponds to the poem line and
    the value of the array index denotes which other lines that line rhymes with.

    :param stripped_body: The poem body (not including title) with no blank lines
    :return: An array denoting all subsequent lines a given line rhymes with
    """

    rhyme_scheme = [-1] * (len(stripped_body) - 1)

    ending_words = []

    i = 0
    while i < len(stripped_body):

        line = stripped_body[i]
        line_as_array = line.split(" ")
        ending_words.append(line_as_array[-1])

        i += 1

    j = 0
    while j < len(ending_words) - 1:

        rhymes = []
        k = j

        while k < len(ending_words) - 1:

            if ending_words[k] in pronouncing.rhymes(ending_words[j]):

                rhymes.append(k)

            k += 1;

        rhyme_scheme[j] = rhymes
        j += 1

    return rhyme_scheme


class Poem:
    """

    Class representing a poem read from the internet.

    The class includes attributes of: the poem's name as a string; the poem's word frequencies stored as a dictionary;
    the poem's rhyme scheme stored as a list of arrays; the poem's syllable count stored as a list; the line count as an
    int; and the number of stanzas as an int.
    """

    def __init__(self, url):
        """Create an instance of a poem given the URL of the poem"""

        poem_as_array = read_poem(url)

        self.name = poem_as_array[0]
        self.line_count = count_lines(poem_as_array)
        self.body = poem_as_array[1:]
        self.stanzas = count_stanzas(poem_as_array)
        self.stripped_body = strip_poem_body(poem_as_array)
        self.end_rhyme_scheme = find_end_rhymes(self.stripped_body)
        self.syllable_count = count_syl(self.stripped_body)

    def __str__(self):
        p = self.name

        return p

    def __repr__(self):
        return str(self) + "\nWord Frequencies: " + str(self.word_occurences) + "\nRhyme: " + self.rhyme_scheme

