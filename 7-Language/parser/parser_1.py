import nltk
import sys
from nltk.tokenize import wordpunct_tokenize
from nltk.tree import Tree

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red" | "wide"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself" | "street"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat" | "saw"
V -> "smiled" | "tell" | "were"
"""
#S -> NP | NP VP | S Conj S


 #NP VP VP NP
 # | NP NP | NP VP VP  
NONTERMINALS = """

S -> NP VP | NP VP Conj VP | NP | NP VP Conj NP VP |NP VP Conj NP VP PP | NP VP PP

NP -> N | Det N | Adj N | AdjP N | Det N | AdjP N
VP -> V | V NP | V NP PP | Conj VP | Adv V | Adv VP  | V PP | NP V PP | V Adv | VP Adv
AdjP -> Adj | Det Adj | Det Adj Adj | Det Adj Adj Adj
PP -> P NP |

"""

# NP -> N | N NP | Det NP | AdjP NP | N PP | P NP | Adv NP | Conj NP 
# VP -> V |  V NP | V NP PP
# AdjP -> Adj | Adj AdjP
# PP -> P NP  

# S -> NP | NP VP | VP
# S -> NP NP | VP Adj | VP P 
# S -> VP AP | AP | VP AP | VP AP VP
# S -> VP AP

# NP -> Det N | N | Det AP N | NP P N | Det N
# VP -> V | V NP | VP VP | N V | N V P | Conj VP | V Det | NP V
# AP -> Det AP | Adj NP | P AP 
# CP -> Conj NP

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = wordpunct_tokenize(sentence)
    res = []
    for word in words:
        if word.isalpha():
            res.append(word.lower())

    return res



def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # max_depth = len(subtree)
    # res = []
    # for subtree in tree.subtrees(lambda t: t.label() == 'NP'):
    #     print(subtree)
        # for s in subtree.subtrees(lambda t: t.label() == 'NP'):
        #     print(s)
        
        # if len(subtree) == 1:
        #     res.append(subtree)
    
    
    res = []

    # Convert Tree to Parented Tree
    ptree = nltk.tree.ParentedTree.convert(tree)

    # Iterate through all subtrees in the tree:
    for subtree in ptree.subtrees(lambda t: t.label() == 'N'):
        print(subtree)
        
        if subtree.parent().parent().label() == "NP":
            res.append(subtree.parent().parent())
        else:
            res.append(subtree.parent())

    return res
    
    


if __name__ == "__main__":
    main()
