"""
Student code for Word Wrangler game
"""

import urllib2
#import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_lst = []
    for item in list1:
        if item not in new_lst:
            new_lst.append(item)
    return new_lst


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_lst = []
    for item in list1:
        if item in list2:
            new_lst.append(item)
            # c = [x for x in list1 if x in list2]
    return new_lst


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    lsti = 0
    lstj = 0
    new_lst = []
    # while (list1 and list2):
    while (lsti < len(list1) and lstj < len(list2)):
        if list1[lsti] <= list2[lstj]:
            # item = list1.pop()
            # print "a", list1[lsti]
            new_lst.append(list1[lsti])
            lsti += 1
            # print lsti
        else:
            # item = list2.pop(_j)
            # print "b", list2[lstj]
            new_lst.append(list2[lstj])
            lstj += 1
    new_lst.extend(list1[lsti:] if lsti < len(list1) else list2[lstj:])
    return new_lst


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    result = []
    if len(list1) < 2:
        return list1
    mid = len(list1) // 2
    left = merge_sort(list1[:mid])
    right = merge_sort(list1[mid:])
    print "left", left
    print "right", right
    while len(left) > 0 or len(right) > 0:
        if len(left) > 0 and len(right) > 0:
            if left[0] > right[0]:
                result.append(right[0])
                right.pop(0)
            else:
                result.append(left[0])
                left.pop(0)
        elif len(right) > 0:
            for item in right:
                result.append(right[0])
                right.pop(0)
        else:
            for item in left:
                result.append(item)
                left.pop(0)
    return result


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """

    if len(word) == 0:
        return [""]
    first = word[0:1]
    rest = word[1:]
    print "first", first
    print "rest", rest
    result = gen_all_strings(rest)
    rest_str = list(result)
    print "rest_strings=", rest_str
    for _string in rest_str:
        print "_string=", _string, "first=", first
        for index in range(len(_string)):
            new_str = _string[:index] + first + _string[index:]
            result.append(new_str)
            print "resultx=", result
        result.append(_string + first)
    print "result=", result
    return result


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_lst = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        word_lst.append(line[:-1])
    return word_lst


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)


# Uncomment when you are ready to try the game
# run()
print merge([3, 4, 5], [3, 4, 5])
# print merge([1,2,3], [])
# list1 = [5, 2, 51, 1, 3, 2]
##print "test", list1.remove("1")
# list2 = [3, 7, 51]
# print remove_duplicates(list1)
# print intersect(list1, list2)
# print "merge=", merge(list1, list2)
# print merge_sort(list1)
# word = "aab"
# print "out=", gen_all_strings(word)
