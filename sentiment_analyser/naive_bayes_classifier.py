from random import shuffle

from preprocessing import preprocessor

from nltk.corpus import movie_reviews 
from nltk import FreqDist
from nltk import NaiveBayesClassifier
from nltk import classify 
from nltk.corpus import stopwords 
import string 


def find_word_from_training_set(comment_words, features):

    print("Comment: {}".format(comment_words))
    #print("len of comment features: {}".format(len(features)))
    
    #print(features)
    
def print_statistics(probability_result, nb_classifier):
                
    print (probability_result.max()) #Output
    print ("Probability of negative: {}".format(probability_result.prob("neg"))) #Probability for the comment being negative.
    print ("Probability of negative: {}".format(probability_result.prob("pos"))) #Probability for the comment being positive.
    #print (nb_classifier.show_most_informative_features(10)) #Most 10 informative words (features)

def test_classifier(classifier, validation_data_set):
    '''Return classifier accuracy'''
    
    classifier_accuracy = classify.accuracy(classifier, validation_data_set)
    print(classifier_accuracy)
    return classifier_accuracy
    
def train_NB_Classifier(training_data_set):
    """Train Naive Bayes classifier with created training data set"""
    
    naive_bayes_classifier = NaiveBayesClassifier.train(training_data_set)
    return naive_bayes_classifier
    
def create_word_feature_set(document, features):
    """Create word feature set to train the classifier"""
    
    words = set(document)
    feature_set = {}
    
    for word in features:
        feature_set[word] = (word in words)
    
    #print(feature_set)
    return feature_set

def get_frequency_distribution(all_words):
    """Count how many times each word occur in the dataset"""
    frequency_distribution = FreqDist(all_words)
    #print (frequency_distribution.most_common(10))
    return frequency_distribution
    
def get_all_words():
    """Get all words from the movie review list"""
    
    all_words = []
    for word in movie_reviews.words():
        all_words.append(word.lower())
    return all_words    
    
def get_features():
    """Get word features of 10 words out of common_word_limit (2000) most common words"""
    
    #frequency_distribution = get_frequency_distribution(normalized_all_words)
    
    #Collect positive reviews:
    positive_reviews = []
    for id in movie_reviews.fileids('pos'):
        words = movie_reviews.words(id)
        for word in words:
            positive_reviews.append(word.lower())

    #Collect negative reviews:
    negative_reviews = []
    for id in movie_reviews.fileids('neg'):
        words = movie_reviews.words(id)
        for word in words:
            negative_reviews.append(word.lower())
    
    #Clean the reviews
    filt_neg_revs = preprocessor.filter_stopwords(negative_reviews)
    filt_pos_revs = preprocessor.filter_stopwords(positive_reviews)
    
    normalized_all_words_neg = preprocessor.normalize_and_clean_comment(filt_neg_revs)
    normalized_all_words_pos = preprocessor.normalize_and_clean_comment(filt_pos_revs)
    
    #frequency_distribution_neg = get_frequency_distribution(normalized_all_words_neg)
    #frequency_distribution_pos = get_frequency_distribution(normalized_all_words_pos)
    
    #Create bag of words from all words:
    #all_words = get_all_words()
    #stopword_filtered_all_words = preprocessor.filter_stopwords(all_words)
    #normalized_all_words = preprocessor.normalize_and_clean_comment(stopword_filtered_all_words)
    #bag_of_words(normalized_all_words)

    #positive reviews feature set
    pos_reviews_set = []
    for words in normalized_all_words_neg:
        pos_reviews_set.append((bag_of_words(words), 'pos'))
     
    #negative reviews feature set
    neg_reviews_set = []
    for words in normalized_all_words_neg:
        neg_reviews_set.append((bag_of_words(words), 'neg'))    
    
    #Shuffle sets
    shuffle(pos_reviews_set)
    shuffle(neg_reviews_set)
    
    print (len(pos_reviews_set))
    print (len(neg_reviews_set))
    #common_word_number_limit = 1000
    
    #common_words_neg = frequency_distribution_neg.most_common(common_word_number_limit)
    #common_words_pos = frequency_distribution_pos.most_common(common_word_number_limit)
    
    #common_words = common_words_neg + common_words_pos
    
    #feature = []
    
    #for word_tuple in common_words:
    #    feature.append(word_tuple[0])
    
    #return feature
    return pos_reviews_set, neg_reviews_set
    
def movie_reviews_to_document_list():
    """Use nltk movie review corpus to train and test the NB classifier
       Total number of reviews is 2000
       First 1000 reviews are positive reviews
       Last  1000 reviews are negative reviews
    """
    
    documents = []
 
    for sentiment in movie_reviews.categories():
        for id in movie_reviews.fileids(sentiment):
            documents.append((movie_reviews.words(id), sentiment))
     
    shuffle(documents)
    return documents

def bag_of_words(words_clean):

    #words_clean = []
    #stopwords_english = stopwords.words('english')
    
    #for word in clean_words:
    #    word = word.lower()
    #    if word not in stopwords_english and word not in string.punctuation:
    #        words_clean.append(word)
    words_dictionary = {}
    print("words_clean len: {}".format(len(words_clean)))
    counter = 0
    for word in words_clean:
        words_dictionary[word] = True
        #print("test{}".format(counter))
        counter += 1
    
    #words_dictionary = dict([word, True] for word in words_clean)
    
    return words_dictionary
    
    
def configure_classifier():
    
    '''REFERENCE: http://blog.chapagain.com.np/python-nltk-sentiment-analysis-on-movie-reviews-natural-language-processing-nlp/'''
    
    documents = movie_reviews_to_document_list()
    #feature_sets = []
    pos_reviews_set, neg_reviews_set = get_features()
   
    #for (document, sentiment) in documents:
    #    f_set = (create_word_feature_set(document, features), sentiment)
    #    feature_sets.append(f_set)
    
    #shuffle(feature_sets)
    
    #TEST DATA SPLIT:
    #validation_data_set = feature_sets[:400]
    #training_data_set = feature_sets[400:]
    test_set = pos_reviews_set[:200] + neg_reviews_set[:200]
    training_data_set = pos_reviews_set[200:] + neg_reviews_set[200:]
    
    print(len(test_set),  len(training_data_set)) # Output: (400, 1600)

    #TRAINING:
    nb_classifier = train_NB_Classifier(training_data_set)
    
    #VALIDATION:
    classifier_accuracy = test_classifier(nb_classifier, test_set)

    return nb_classifier, classifier_accuracy, features