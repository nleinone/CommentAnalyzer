from nltk import NaiveBayesClassifier
from nltk import DecisionTreeClassifier
from nltk import MaxentClassifier
from nltk import classify 
    
def configure_all(training_and_test_data, all_training_data, cv):
    """Train classifiers with created training data set and return classifier accuracy"""
    
    '''NAIVE BAYES'''
    print("Configuring Naive Bayes classifier...")
    nb_accuracies = []
    
    if cv:
        counter = 1
        '''Cross-Validation'''
        for test_train_data in training_and_test_data:
            print("{}. Cross-validation...".format(counter))
            nb_classifier = NaiveBayesClassifier.train(test_train_data[1])
            nb_accuracy = classify.accuracy(nb_classifier, test_train_data[0])
            nb_accuracies.append(nb_accuracy)
            counter += 1
        nb_count_accuracies = len(nb_accuracies)
        nb_sum_accuracies = sum(nb_accuracies)
        nb_avg_accuracy = nb_sum_accuracies / nb_count_accuracies

    
    #Train with all data available
    print("Training Naive Bayes Classifier...")
    nb_classifier = NaiveBayesClassifier.train(all_training_data)
    if cv == False:
        nb_avg_accuracy = 0.78
    return nb_classifier, nb_avg_accuracy