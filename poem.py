"""
This class functions to read 43 poems listed as the "best poems" by the website
Lit Hub. The class creates an instance of a poem for each poem which includes attributes
for the poem's word frequencies, the rhyme scheme, syllable count, line count, and stanzas.

NOTE: read_poem code was adapted from code developed in a group project with Sam Rousell and Gerard Goucher. The code
was originally written by Sam and the general framework was given by his code.
"""
from bs4 import BeautifulSoup
import requests as rq
from string import punctuation


def read_poem(address):
    p_readable = ""

    site = rq.get(address)

    soup = BeautifulSoup(site.text, 'html.parser')
    title = soup.h1.text

    p_readable += title.strip()

    body = soup.find('div', attrs={"class": "c-feature-bd"}).text

    print("TEXT:")

    for line in body:

        print(line)
        p_readable += line

    print(p_readable)





class Poem:
    """

    Class representing a poem read from the internet.

    The class includes attributes of: the poem's name as a string; the poem's word frequencies stored as a dictionary;
    the poem's rhyme scheme stored as a list of arrays; the poem's syllable count stored as a list; the line count as an
    int; and the number of stanzas as an int.
    """

    def __init__(self, url):
        """Create an instance of a poem given the URL of the poem"""

        p_read = read_poem(url)

        self.name = p_read[0]

    def __str__(self):
        p = self.name

        return p

    def __repr__(self):
        return str(self) + "\nWord Frequencies: " + str(self.word_occurences) + "\nRhyme: " + self.rhyme_scheme


test_poem = Poem("https://www.poetryfoundation.org/poems/52167/errata")
print(test_poem.name)