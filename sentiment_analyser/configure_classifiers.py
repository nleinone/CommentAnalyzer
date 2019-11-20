from nltk import NaiveBayesClassifier
from nltk import classify 

import collections
from nltk.metrics.scores import precision, recall, f_measure

'''
Recall and precision reference:
https://streamhacker.com/2010/05/17/text-classification-sentiment-analysis-precision-recall/
'''
def calculate_mean_values(nb_accuracies, pos_mean_precision, pos_mean_recall, pos_mean_f_score, neg_mean_precision, neg_mean_recall, neg_mean_f_score):
    '''Calculate mean values of accuracy, precision, recall, and f1-score for neg and pos sentiment.'''
    
    nb_count_accuracies = len(nb_accuracies)
    nb_sum_accuracies = sum(nb_accuracies)
    mean_nb_accuracy = nb_sum_accuracies / nb_count_accuracies
    
    count_precision = len(pos_mean_precision)
    sum_precision = sum(pos_mean_precision)
    mean_pos_mean_precision = sum_precision / count_precision
    
    count_recall = len(pos_mean_recall)
    sum_recall = sum(pos_mean_recall)
    mean_pos_mean_recall = sum_recall / count_recall
    
    count_f_score = len(pos_mean_f_score)
    sum_f_score = sum(pos_mean_f_score)
    mean_pos_mean_f_score = sum_f_score / count_f_score
    
    count_precision = len(neg_mean_precision)
    sum_precision = sum(neg_mean_precision)
    mean_neg_mean_precision = sum_precision / count_precision
    
    count_recall = len(neg_mean_recall)
    sum_recall = sum(neg_mean_recall)
    mean_neg_mean_recall = sum_recall / count_recall
    
    count_f_score = len(neg_mean_f_score)
    sum_f_score = sum(neg_mean_f_score)
    mean_neg_mean_f_score = sum_f_score / count_f_score
    
    return mean_nb_accuracy, mean_pos_mean_precision, mean_pos_mean_recall, mean_pos_mean_f_score, mean_neg_mean_precision, mean_neg_mean_recall, mean_neg_mean_f_score
    
    
def calculate_precision_and_recall(nb_classifier, train_data, test_data):
    '''Calculate precision, recall and f1-score for negative and positive sentiment probability'''

    reference_sets = collections.defaultdict(set)
    test_sets = collections.defaultdict(set)
    
    for index, (features, label) in enumerate(test_data):
        reference_sets[label].add(index)
        observed = nb_classifier.classify(features)
        test_sets[observed].add(index)
    
    pos_precision = precision(reference_sets['pos'], test_sets['pos'])
    pos_recall = recall(reference_sets['pos'], test_sets['pos'])
    pos_f_score = recall(reference_sets['pos'], test_sets['pos'])
    
    neg_precision = precision(reference_sets['neg'], test_sets['neg'])
    neg_recall = recall(reference_sets['neg'], test_sets['neg'])
    neg_f_score = recall(reference_sets['neg'], test_sets['neg'])
    
    return pos_precision, pos_recall, pos_f_score, neg_precision, neg_recall, neg_f_score

def configure_all(training_and_test_data, all_training_data, cv):
    """Train classifiers with created training data set and return classifier accuracy"""
    
    '''NAIVE BAYES'''
    print("Configuring Naive Bayes classifier...")
    nb_accuracies = []
    
    pos_mean_precision = [] 
    pos_mean_recall = []
    pos_mean_f_score = []
    
    neg_mean_precision = [] 
    neg_mean_recall = []
    neg_mean_f_score = []
    
    if cv:
        counter = 1
        '''Cross-Validation for accuracy, precision and recall'''
        for test_train_data in training_and_test_data:
            print("{}. Cross-validation...".format(counter))
            
            train_data = test_train_data[1]
            test_data = test_train_data[0]
            
            nb_classifier = NaiveBayesClassifier.train(train_data)
            nb_accuracy = classify.accuracy(nb_classifier, test_data)
            nb_accuracies.append(nb_accuracy)
            counter += 1
            
            pos_precision, pos_recall, pos_f_score, neg_precision, neg_recall, neg_f_score = calculate_precision_and_recall(nb_classifier, train_data, test_data)
            
            pos_mean_precision.append(pos_precision)
            pos_mean_recall.append(pos_recall)
            pos_mean_f_score.append(pos_f_score)
            
            neg_mean_precision.append(neg_precision)
            neg_mean_recall.append(neg_recall)
            neg_mean_f_score.append(neg_f_score)
        
        mean_nb_accuracy, mean_pos_mean_precision, mean_pos_mean_recall, mean_pos_mean_f_score, mean_neg_mean_precision, mean_neg_mean_recall, mean_neg_mean_f_score = calculate_mean_values(nb_accuracies, pos_mean_precision, pos_mean_recall, pos_mean_f_score, neg_mean_precision, neg_mean_recall, neg_mean_f_score)
        
        average_values = {'mean_accuracy': mean_nb_accuracy, 'mean_pos_mean_precision':mean_pos_mean_precision,'mean_pos_mean_recall':mean_pos_mean_recall,'mean_pos_mean_f_score':mean_pos_mean_f_score,'mean_neg_mean_precision':mean_neg_mean_precision,'mean_neg_mean_recall':mean_neg_mean_recall,'mean_neg_mean_f_score':mean_neg_mean_f_score}
        
    #Train with all data available
    print("Training Naive Bayes Classifier...")
    nb_classifier = NaiveBayesClassifier.train(all_training_data)
    if cv == False:
        average_values = {}
        average_values['mean_accuracy'] = 0.85 #With stemming and cross validation
    return nb_classifier, average_values