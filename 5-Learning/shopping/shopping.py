import csv
import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def month_label_to_number(label):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(label)



def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    with open('shopping.csv', newline='') as csvfile:
        data_row = csv.reader(csvfile, delimiter=' ', quotechar='|')
        header = next(data_row)
        evidence = []
        labels = []


        for row in data_row:
            values_list  = row[0].split(',')
            values_list[10] = month_label_to_number(values_list[10])
            values_list[15] = '1' if values_list[15] == "Returng_Visitor" else '0'
            values_list[16] = '1' if values_list[16] == 'TRUE' else '0'
            values_list[17] = '1' if values_list[17] == "TRUE" else '0'
            values_list = [int(valor) if isinstance(valor, str) and '.' not in valor else float(valor) if isinstance(valor, str) else valor for valor in values_list]
            evidence.append(values_list[0:-1])  
            labels.append(values_list[-1])
        
    return (evidence, labels)
    


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    knc = KNeighborsClassifier(n_neighbors=1)
    knc.fit(evidence, labels)
    return knc


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    right_ones = 0
    right_zeros = 0
    total_zeros = labels.count(0)
    total_ones = len(labels) - total_zeros

    


    for index, n in enumerate(labels):
        if n == 0 and predictions[index] == 0:
            right_zeros += 1
        if n == 1 and predictions[index] == 1:
            right_ones += 1

    

    true_pos_rate = (right_ones) / total_ones
    true_neg_rate = (right_zeros) / total_zeros
    



    return (true_pos_rate, true_neg_rate)

if __name__ == "__main__":
    main()
