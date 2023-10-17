from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(Not(And(AKnave, AKnight)), (AKnave))



    # Implication(Not(AKnight), AKnave),
    # Implication(Not(And(AKnave, AKnight)), (AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Implication(AKnight, And(AKnave, BKnave))
    
    
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    
    Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnave, BKnight),
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight,BKnave))),
    Implication(BKnave, And(AKnave, BKnave))



    # Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # Implication(AKnave, Or(Or(AKnight, BKnave), Or(BKnight, AKnave))),
    # Implication(BKnight, Or(Or(AKnight, BKnave), Or(BKnight, AKnave))),
    # Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))),


    # Or(Or(And(AKnight, BKnight), And(AKnave, BKnave)), And(AKnight, BKnave), And(AKnave, BKnight)),
    # Implication(AKnight,  Not(BKnave)),
    # Implication(AKnave,  Not(BKnave)),
    # Implication(BKnight,  AKnave),
    # Implication(BKnave,  AKnave),

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO

    Or(AKnight, AKnave),
    Implication(AKnave, CKnight),
    Implication(AKnight, BKnave),
    Implication(BKnight, And(AKnave,CKnave)),
    Implication(BKnave, And(Or(AKnight, AKnave),CKnight)),
    Implication(CKnight, And(AKnight, BKnave)),
    Implication(CKnave, And(AKnave, BKnight)),
    
    





    # Or(And(CKnight, AKnight), And(BKnight, CKnight)),
    # Implication(BKnave, Or(AKnave, AKnight)),
    # Implication(AKnave, CKnave),
    # Implication(BKnave, And(AKnight, CKnight) ), #Certo
    # Biconditional(CKnight, And(AKnight, BKnave)),
    # Implication(Not(CKnight), AKnave),
    # Implication(AKnight, BKnave)



   



)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            # print(knowledge.formula())
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
