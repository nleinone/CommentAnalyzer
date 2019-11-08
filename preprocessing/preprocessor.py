import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def normalize_and_clean_comment(stopword_filtered_comment):
    """Make all words lowercase and clean words which are not alphabetic"""
    
    cleaned_comment = []
    
    for comment in stopword_filtered_comment:
        single_comment = []
        for word in comment:
            if word.isalpha():
                single_comment.append(word.lower())
        if len(single_comment) != 0:
            cleaned_comment.append(single_comment)
    
    return cleaned_comment
    
def filter_stopwords(tokenized_answer, training_mode):
    '''Filter stopwords'''
    
    stop_words = set(stopwords.words('english'))
    
    stopword_filtered_answer = []

    if training_mode:
        for comment in tokenized_answer:
            single_comment = []
            for word in comment:
                if word not in stop_words:
                    single_comment.append(word)
            if len(single_comment) != 0:
                stopword_filtered_answer.append(single_comment)  
    
    else:
        single_comment = []
        for word in tokenized_answer:
            if word not in stop_words:
                single_comment.append(word)
        if len(single_comment) != 0:
            stopword_filtered_answer.append(single_comment)
    
    return stopword_filtered_answer
    
def tokenize_comment(user_answer):
    '''Tokenize user answer'''
    
    tokenized_answer = nltk.word_tokenize(user_answer)
    return tokenized_answer