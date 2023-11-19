import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    # if len(sys.argv) != 2:
    if len(sys.argv) != 1: # DESC?OENTAR O DE CIMA ANTES DE CMANDAR

        sys.exit("Usage: python heredity.py data.csv")
    # people = load_data(sys.argv[1])
    people = load_data("./data/family0.csv")

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

#one_gene=
def joint_probability(people, one_gene, two_genes, have_trait):
    # one_gene = {"Harry"}
    # two_genes = {"James"}
    # have_trait = {"James"}
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    res = {}
    jp = 1
    # Calcula as probabilidades de quem nao tem pai nem mae
    for key, value in people.items():
        if value['father'] == None and value['mother'] == None:
            if key not in one_gene and key not in two_genes:
                gen_prob = PROBS["gene"][0]
                if key not in have_trait:
                    trait_prob = PROBS["trait"][0][False]
                else:
                    trait_prob = PROBS["trait"][0][True]
                res[key] = round(gen_prob*trait_prob, 4)
                jp *= round(gen_prob*trait_prob, 4)

            elif key in one_gene:
                gen_prob = PROBS["gene"][1]
                if key not in have_trait:
                    trait_prob = PROBS["trait"][1][False]
                else:
                    trait_prob = PROBS["trait"][1][True]
                res[key] = round(gen_prob*trait_prob, 4)
                jp *= round(gen_prob*trait_prob, 4)

            elif key in two_genes:
                gen_prob = PROBS["gene"][2]
                if key not in have_trait:
                    trait_prob = PROBS["trait"][2][False]
                else:
                    trait_prob = PROBS["trait"][2][True]
                res[key] = round(gen_prob*trait_prob, 4)
                jp *= round(gen_prob*trait_prob, 4)

    for key, value in people.items():
        if value['father'] != None and value['mother'] != None:
            if key not in one_gene and key not in two_genes:
                if value['mother'] not in one_gene and value['mother'] not in two_genes:
                    mother_pb_pass_gene = PROBS["mutation"]
                    mother_pb_not_pass_gene = 1 - PROBS["mutation"]
                if value['mother'] in one_gene:
                    mother_pb_pass_gene = round(.5* (1 - PROBS['mutation']), 4)     #####################
                    mother_pb_not_pass_gene = round(.5 * PROBS['mutation'], 4)##CONFERIR ESSA PARTE
                if value['mother'] in two_genes:
                    mother_pb_pass_gene =1 - (PROBS["mutation"])
                    mother_pb_not_pass_gene =  PROBS['mutation']
                if value['father'] not in one_gene and value['father'] not in two_genes:
                    father_pb_pass_gene = PROBS["mutation"]
                    father_pb_not_pass_gene = 1 - PROBS["mutation"]
                if value['father'] in one_gene:
                    father_pb_pass_gene = round(.5* (1 - PROBS['mutation']), 4)      #####################
                    father_pb_not_pass_gene = round(.5 * PROBS['mutation'], 4) ##CONFERIR ESSA PARTE
                if value['father'] in two_genes:
                    father_pb_pass_gene =1 - (PROBS["mutation"])
                    father_pb_not_pass_gene =  PROBS['mutation']
                if key not in have_trait:
                    res[key] = round((mother_pb_not_pass_gene*father_pb_not_pass_gene)*PROBS["trait"][0][False], 4)
                    jp *= round((mother_pb_not_pass_gene*father_pb_not_pass_gene)*PROBS["trait"][0][False], 4)
                else:
                    res[key] = round((mother_pb_not_pass_gene*father_pb_not_pass_gene)*PROBS["trait"][0][True], 4)
                    jp *= round((mother_pb_not_pass_gene*father_pb_not_pass_gene)*PROBS["trait"][0][True], 4)

            if key in one_gene:
                if value['mother'] not in one_gene and value['mother'] not in two_genes:
                    mother_pb_pass_gene = PROBS["mutation"]
                    mother_pb_not_pass_gene = 1 - PROBS["mutation"]
                if value['mother'] in one_gene:
                    mother_pb_pass_gene = round(.5* (1 - PROBS['mutation']), 4)     #####################
                    mother_pb_not_pass_gene = round(.5 * PROBS['mutation'], 4)##CONFERIR ESSA PARTE
                if value['mother'] in two_genes:
                    mother_pb_pass_gene =1 - (PROBS["mutation"])
                    mother_pb_not_pass_gene =  PROBS['mutation']
                if value['father'] not in one_gene and value['father'] not in two_genes:
                    father_pb_pass_gene = PROBS["mutation"]
                    father_pb_not_pass_gene = 1 - PROBS["mutation"]
                if value['father'] in one_gene:
                    father_pb_pass_gene = round(.5* (1 - PROBS['mutation']), 4)      #####################
                    father_pb_not_pass_gene = round(.5 * PROBS['mutation'], 4) ##CONFERIR ESSA PARTE
                if value['father'] in two_genes:
                    father_pb_pass_gene =1 - (PROBS["mutation"])
                    father_pb_not_pass_gene =  PROBS['mutation']
                if key not in have_trait:
                    res[key] = (((mother_pb_not_pass_gene*father_pb_pass_gene) + (father_pb_not_pass_gene * mother_pb_pass_gene)) * PROBS["trait"][1][False])
                    jp *= (((mother_pb_not_pass_gene*father_pb_pass_gene) + (father_pb_not_pass_gene * mother_pb_pass_gene)) * PROBS["trait"][1][False])

                else:
                    res[key] = (((mother_pb_not_pass_gene*father_pb_pass_gene) + (father_pb_not_pass_gene * mother_pb_pass_gene)) * PROBS["trait"][1][True])
                    jp *= (((mother_pb_not_pass_gene*father_pb_pass_gene) + (father_pb_not_pass_gene * mother_pb_pass_gene)) * PROBS["trait"][1][True])


            if key in two_genes:
                if value['mother'] not in one_gene and value['mother'] not in two_genes:
                    mother_pb_pass_gene = PROBS["mutation"]
                    mother_pb_not_pass_gene = 1 - PROBS["mutation"]
                if value['mother'] in one_gene:
                    mother_pb_pass_gene = round(.5* (1 - PROBS['mutation']), 4)      #####################
                    mother_pb_not_pass_gene = round(.5 * PROBS['mutation'], 4)##CONFERIR ESSA PARTE
                if value['mother'] in two_genes:
                    mother_pb_pass_gene =1 - (PROBS["mutation"])
                    mother_pb_not_pass_gene =  PROBS['mutation']
                if value['father'] not in one_gene and value['father'] not in two_genes:
                    father_pb_pass_gene = PROBS["mutation"]
                    father_pb_not_pass_gene = 1 - PROBS["mutation"]
                if value['father'] in one_gene:
                    father_pb_pass_gene = round(.5* (1 - PROBS['mutation']), 4)       #####################
                    father_pb_not_pass_gene = round(.5 * PROBS['mutation'], 4) ##CONFERIR ESSA PARTE
                if value['father'] in two_genes:
                    father_pb_pass_gene =1 - (PROBS["mutation"])
                    father_pb_not_pass_gene =  PROBS['mutation']
                if key not in have_trait:
                    res[key] = round(((mother_pb_pass_gene*father_pb_pass_gene) + (father_pb_pass_gene * mother_pb_pass_gene)) * PROBS["trait"][2][False], 4)
                    jp *= round(((mother_pb_pass_gene*father_pb_pass_gene) + (father_pb_pass_gene * mother_pb_pass_gene)) * PROBS["trait"][2][False], 4)

                else:
                    res[key] = round(((mother_pb_not_pass_gene*father_pb_pass_gene) + (father_pb_not_pass_gene * mother_pb_pass_gene)) * PROBS["trait"][2][True], 4)
                    jp *= round(((mother_pb_not_pass_gene*father_pb_pass_gene) + (father_pb_not_pass_gene * mother_pb_pass_gene)) * PROBS["trait"][2][True], 4)


    aws = 1
    
            
    return jp


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    p = round(p, 4)
    for key, value in probabilities.items():
        if key in one_gene:
            probabilities[key]['gene'][1] += p
            probabilities[key]['gene'][1] = (probabilities[key]['gene'][1])
        elif key in two_genes:
            probabilities[key]['gene'][2] += p
            probabilities[key]['gene'][2] = (probabilities[key]['gene'][2])
        else:
            probabilities[key]['gene'][0] += p
            probabilities[key]['gene'][0] = (probabilities[key]['gene'][0])
        
        if key in have_trait:
            probabilities[key]['trait'][True] += p
            probabilities[key]['trait'][True] = (probabilities[key]['trait'][True])
        else:
            probabilities[key]['trait'][False] += p
            probabilities[key]['trait'][False] = (probabilities[key]['trait'][False])



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    for key, value in probabilities.items():
        total_gene = 0
        total_trait = 0
        for gene in value['gene']:
            total_gene += value['gene'][gene]
            
        for trait in value['trait']:
            total_trait += value['trait'][trait]
        
        probabilities[key]['gene'][0] = round((value['gene'][0] * 100) / total_gene, 2)
        probabilities[key]['gene'][1] = round((value['gene'][1] * 100) / total_gene, 2)
        probabilities[key]['gene'][2] = round((value['gene'][2] * 100) / total_gene, 2)
        
        probabilities[key]['trait'][True] = round((value['trait'][True] * 100) / total_trait, 2)
        probabilities[key]['trait'][False] = round((value['trait'][False] * 100) / total_trait, 2)
        
        

         



if __name__ == "__main__":
    main()
