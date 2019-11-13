from nltk import NaiveBayesClassifier
from nltk import DecisionTreeClassifier
from nltk import MaxentClassifier
from nltk import classify 

def pv(value1):
    
    print("Value: {}\n".format(value1))
    
def configure_all(training_and_test_data):
    """Train classifiers with created training data set and return classifier accuracy"""
    
    '''NAIVE BAYES'''
    print("Configuring Naive Bayes classifier...")
    nb_accuracies = []
    for test_train_data in training_and_test_data:    
        nb_classifier = NaiveBayesClassifier.train(test_train_data[1])
        nb_accuracy = classify.accuracy(nb_classifier, test_train_data[0])
        nb_accuracies.append(nb_accuracy)
        
    nb_count_accuracies = len(nb_accuracies)
    nb_sum_accuracies = sum(nb_accuracies)
    nb_avg_accuracy = nb_sum_accuracies / nb_count_accuracies
    
    '''DECISION TREE
    print("Configuring Decision Tree classifier...")
    #[test, training]
    dt_accuracies = []
    counter = 0
    pv(len(training_and_test_data))
    #traindata = test_train_data[1]
    #pv(len(traindata)) #reviews + labels
    #pv(len(traindata[0])) #one review + label
    #pv(traindata[0][0]) #review
    #pv(traindata[0][1]) #label
    
    for test_train_data in training_and_test_data:
        print(len(test_train_data[1]))
        print(len(test_train_data[1][0]))
        dt_classifier = DecisionTreeClassifier.train(test_train_data[1], binary = True)
        dt_accuracy = classify.accuracy(dt_classifier, test_train_data[0])
        dt_accuracies.append(dt_accuracy)
        counter += 1
    
    """MAXENT CLASSIFIER"""
    me_accuracies = []
    print("Configuring Maxent classifier...")
    for test_train_data in training_and_test_data:
        
        me_classifier = MaxentClassifier.train(test_train_data[1])
        me_accuracy = classify.accuracy(me_classifier, test_train_data[0])
        me_accuracies.append(me_accuracy)
        
    me_count_accuracies = len(me_accuracies)
    me_sum_accuracies = sum(me_accuracies)
    me_avg_accuracy = me_sum_accuracies / me_count_accuracies
    '''
    
    return nb_classifier, nb_avg_accuracy