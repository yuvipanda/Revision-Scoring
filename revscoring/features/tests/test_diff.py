from nose.tools import eq_

from ... import languages
from ...datasources import diff as diff_datasource
from ...dependent import solve
from ..diff import (badwords_added, badwords_removed, chars_added,
                    chars_removed, longest_repeated_char_added,
                    longest_token_added, markup_chars_added,
                    markup_chars_removed, misspellings_added,
                    misspellings_removed, numeric_chars_added,
                    numeric_chars_removed, segments_added, segments_removed,
                    symbolic_chars_added, symbolic_chars_removed,
                    uppercase_chars_added, uppercase_chars_removed,
                    words_added, words_removed)


################################## Segments ####################################
def test_segments_added():
    cache = {
        diff_datasource.added_segments: ["one", "two", "three"]
    }
    eq_(solve(segments_added, cache=cache), 3)

def test_segments_removed():
    cache = {
        diff_datasource.removed_segments: ["one", "two"]
    }
    eq_(solve(segments_removed, cache=cache), 2)

################################## Characters ##################################
def test_chars_added():
    cache = {
        diff_datasource.added_segments: ["twelve", "letter"]
    }
    eq_(solve(chars_added, cache=cache), 12)

def test_chars_removed():
    cache = {
        diff_datasource.removed_segments: ["fourteen", "letter"]
    }
    eq_(solve(chars_removed, cache=cache), 14)

def test_markup_chars_added():
    cache = {
        diff_datasource.added_segments: ["fo{{ur}}teen", "l[[etter]]"]
    }
    eq_(solve(markup_chars_added, cache=cache), 8)

def test_markup_chars_removed():
    cache = {
        diff_datasource.removed_segments: ["foo[[bar]][HAT]", "{| |}"]
    }
    eq_(solve(markup_chars_removed, cache=cache), 10)


def test_numeric_chars_added():
    cache = {
        diff_datasource.added_segments: ["foo, '\"?.!2 and 43", "Wut"]
    }
    eq_(solve(numeric_chars_added, cache=cache), 3)

def test_numeric_chars_removed():
    cache = {
        diff_datasource.removed_segments: ["foo, '\"?.5!#105$%", "Wut"]
    }
    eq_(solve(numeric_chars_removed, cache=cache), 4)


def test_symbolic_chars_added():
    cache = {
        diff_datasource.added_segments: ["foo, '\"?.!", "Wut"]
    }
    eq_(solve(symbolic_chars_added, cache=cache), 6)

def test_symbolic_chars_removed():
    cache = {
        diff_datasource.removed_segments: ["foo, '\"?.!#$%", "Wut"]
    }
    eq_(solve(symbolic_chars_removed, cache=cache), 9)

def test_uppercase_chars_added():
    cache = {
        diff_datasource.added_segments: ["THIS has 14 UPPER CASE",
                                           "characterS"]
    }
    eq_(solve(uppercase_chars_added, cache=cache), 14)

def test_uppercase_chars_removed():
    cache = {
        diff_datasource.removed_segments: ["THIS has 5 upper case",
                                           "characterS"]
    }
    eq_(solve(uppercase_chars_removed, cache=cache), 5)

def test_longest_repeated_char_added():
    cache = {
        diff_datasource.added_segments: ["THIS has is an aaAa",
                                           "aaa bah"]
    }
    eq_(solve(longest_repeated_char_added, cache=cache), 4)
    cache = {
        diff_datasource.added_segments: []
    }
    eq_(solve(longest_repeated_char_added, cache=cache), 1)

################################ Words #########################################
def test_words_added():
    cache = {
        diff_datasource.added_words: ["Four", "word", "are", "here"]
    }
    eq_(solve(words_added, cache=cache), 4)

def test_words_removed():
    cache = {
        diff_datasource.removed_words: ["Three", "words", "now"]
    }
    eq_(solve(words_removed, cache=cache), 3)

def test_badwords_added():
    def is_badword(w): return w == "badword"
    cache = {
        languages.is_badword: is_badword,
        diff_datasource.added_words: ["Some", "words", "and", "badword"]
    }
    eq_(solve(badwords_added, cache=cache), 1)

def test_badwords_removed():
    def is_badword(w): return w == "badword"
    cache = {
        languages.is_badword: is_badword,
        diff_datasource.removed_words: ["Some", "badword", "and", "badword"]
    }
    eq_(solve(badwords_removed, cache=cache), 2)

def test_misspellings_added():
    def is_misspelled(w): return w == "misspelled"
    cache = {
        languages.is_misspelled: is_misspelled,
        diff_datasource.added_words: ["Some", "misspelled", "and", "misspelled"]
    }
    eq_(solve(misspellings_added, cache=cache), 2)

def test_misspellings_removed():
    def is_misspelled(w): return w == "misspelled"
    cache = {
        languages.is_misspelled: is_misspelled,
        diff_datasource.removed_words: ["Some", "badword", "and", "misspelled"]
    }
    eq_(solve(misspellings_removed, cache=cache), 1)

################################ Tokens ########################################
def test_longest_token_added():
    cache = {
        diff_datasource.added_tokens: ["Some", "badword", "refridgerator"]
    }
    eq_(solve(longest_token_added, cache=cache), len("refridgerator"))
    cache = {
        diff_datasource.added_tokens: []
    }
    eq_(solve(longest_token_added, cache=cache), 1)
