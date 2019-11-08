import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def normalize_and_clean_comment(stopword_filtered_comment):
    """Make all words lowercase and clean words which are not alphabetic"""
    
    cleaned_comment = []
    
    for word in stopword_filtered_comment:
        
        if word.isalpha():
            cleaned_comment.append(word.lower())
        
    #print('cleaned: {}'.format(cleaned_comment))
    
    return cleaned_comment
    
def filter_stopwords(tokenized_answer):
    '''Filter stopwords'''
    
    stop_words = set(stopwords.words('english')) 
    stopword_filtered_answer = []
    
    for word in tokenized_answer:
        if word not in stop_words:
            stopword_filtered_answer.append(word)
            
    #print('filtered: {}'.format(stopword_filtered_answer))
    return stopword_filtered_answer

def tokenize_comment(user_answer):
    '''Tokenize user answer'''
    
    tokenized_answer = nltk.word_tokenize(user_answer)
    #print('tokenized: {}'.format(tokenized_answer))
    return tokenized_answer