import os
from datetime import datetime

from parsing import parsing_functions
from preprocessing import preprocessor
from sentiment_analyser import naive_bayes_classifier

if __name__ == '__main__':
    
    '''Variables'''
    number_of_lines_processed = 0
    
    '''*** INITIAL CONFIGURATIONS ***'''
    #Runtime stamp
    datetime_start = datetime.now()
    
    
    #Configure classifier:
    print("Configuring classifier...")
    nb_classifier, classifier_accuracy = naive_bayes_classifier.configure_classifier()
    '''*** INITIAL CONFIGURATIONS ENDS***'''
    
    '''**** FILE PARSING PROCESS STARTS HERE****'''
    #Fetch csv document
    csv_file_names = parsing_functions.fetch_document_names()
    
    for file_name in csv_file_names:
        
        #Variables
        information_collection = []
        bot_mood_happy_collection = []
        
        #Count file lines
        line_count = parsing_functions.count_file_lines(csv_file_names)
        number_of_lines_processed += line_count
        
        #Convert file lines to list (Max 100)
        file_lines_list = parsing_functions.convert_file_to_list(line_count, file_name)
        
        #Distinguish information from file line (user_name, time, bot_mood, bot_answer, user_answer):
        for file_line in file_lines_list:
            information_dictionary = parsing_functions.distinguish_information(file_line)
            information_collection.append(information_dictionary)
        #print('information_collection: {}\n'.format(information_collection))
        
        happy_bot_comments, happysad_bot_comments, sad_bot_comments, neutral_bot_comments, hello_bot_comments = parsing_functions.separate_comments_by_bot_mood(information_collection)
        all_comments = [happy_bot_comments, happysad_bot_comments, sad_bot_comments, neutral_bot_comments, hello_bot_comments]
        #print(all_comments)
        
        for comment_set in all_comments:
            
            try:
                first_comment = comment_set[0]
                mood = first_comment['bot_mood']
                print('Processing {} bot answer data...'.format(mood))
            except:
                continue
        
            '''*** PARSING ENDS HERE ***'''
            
            '''*** NATURAL LANGUAGE PREPROCESSING STARTS HERE***'''
            
            #Preprocess user comments one bot mood data set at time:
            for comment in comment_set:
                user_answer = comment['user_answer']
                
                #print("user_answer: {}".format(user_answer))
                
                #Tokenize comment
                tokenized_comment = preprocessor.tokenize_comment(user_answer)
                
                #print("tokenized_comment: {}".format(tokenized_comment))
                
                #Filter stopwords
                training_mode = False
                stopword_filtered_comment = preprocessor.filter_stopwords(tokenized_comment, training_mode)
                
                #print("stopword_filtered_comment: {}".format(stopword_filtered_comment))
                
                #Clean the user answer
                normalized_comment = preprocessor.normalize_and_clean_comment(stopword_filtered_comment)
                
                #print("Normalized comment: {}".format(normalized_comment))
                
                '''*** NATURAL LANGUAGE PREPROCESSING STOPS HERE***'''
                
                '''*** SENTIMENT ANALYSIS WITH NAIVE BAYES STARTS HERE***'''

                normalized_comment_feature_set = naive_bayes_classifier.bag_of_words(normalized_comment, training_mode)
                
                #print("normalized_comment_feature_set: {}".format(normalized_comment_feature_set))
                
                probability_result = nb_classifier.prob_classify(normalized_comment_feature_set)
                
                #Print statistics:
                naive_bayes_classifier.print_statistics(probability_result, nb_classifier, normalized_comment_feature_set, user_answer, classifier_accuracy)
                #naive_bayes_classifier.find_word_from_training_set(normalized_comment, normalized_comment_features)
                
    #Runtime stamp
    
    
    print("Runtime: {}\n".format(datetime.now() - datetime_start))
                
                
                
                
                
                
                
                
                
                
                
                
    