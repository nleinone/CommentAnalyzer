import os
from datetime import datetime

from parsing import parsing_functions
from preprocessing import preprocessor
from sentiment_analyser import configure_classifiers
from sentiment_analyser import generate_classifier_data_sets

if __name__ == '__main__':
    #Runtime stamp
    datetime_start = datetime.now()
    '''Variables'''
    number_of_lines_processed = 0
    cross_validations_fold_ratio = 200
    
    '''*** INITIAL CONFIGURATIONS ***'''
    print("Configuring classifiers...")
    
    training_and_test_data, all_training_data = generate_classifier_data_sets.get_training_and_test_data(cross_validations_fold_ratio)
    nb_classifier, nb_avg_accuracy = configure_classifiers.configure_all(training_and_test_data, all_training_data)
    
    classifier = nb_classifier
    classifier_accuracy = nb_avg_accuracy
        
    '''*** INITIAL CONFIGURATIONS ENDS***'''
    
    '''**** FILE PARSING PROCESS STARTS HERE****'''
    #Fetch csv document
    print("test1")
    csv_file_names = parsing_functions.fetch_document_names()
    
    for file_name in csv_file_names:
        print("test2")
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
            print("test3")
            information_dictionary = parsing_functions.distinguish_information(file_line)
            information_collection.append(information_dictionary)
        
        #print(information_collection)
        happy_bot_comments, happysad_bot_comments, sad_bot_comments, neutral_bot_comments, hello_bot_comments = parsing_functions.separate_comments_by_bot_mood(information_collection)
        all_comments = [happy_bot_comments, happysad_bot_comments, sad_bot_comments, neutral_bot_comments, hello_bot_comments]
        print("all comments: ")
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
            print("test4")
            #Preprocess user comments one bot mood data set at time:
            for comment in comment_set:
                print("test5")
                training_mode = False
                user_answer = comment['user_answer']
                
                #Tokenize comment
                tokenized_comment = preprocessor.tokenize_comment(user_answer)
        
                #Filter stopwords for unigram
                bigram = False
                stopword_filtered_comment_unigram = preprocessor.filter_stopwords(tokenized_comment, training_mode, bigram)
                
                #Filter stopwords for bigram
                bigram = True
                stopword_filtered_comment_bigram = preprocessor.filter_stopwords(tokenized_comment, training_mode, bigram)
                
                #Clean the user answer unigram
                normalized_comment_unigram = preprocessor.normalize_and_clean_comment(stopword_filtered_comment_unigram)
                
                #Clean the user answer bigram
                normalized_comment_bigram = preprocessor.normalize_and_clean_comment(stopword_filtered_comment_bigram)
                
                '''*** NATURAL LANGUAGE PREPROCESSING STOPS HERE***'''
                
                '''*** SENTIMENT ANALYSIS WITH NAIVE BAYES STARTS HERE***'''
            
                normalized_comment_feature_set_unigram = generate_classifier_data_sets.extract_feature_unigram(normalized_comment_unigram, training_mode)
                normalized_comment_feature_set_bigram = generate_classifier_data_sets.extract_features_bigram(normalized_comment_bigram, training_mode)
                normalized_comment_feature_set = generate_classifier_data_sets.extract_features(normalized_comment_unigram, normalized_comment_bigram, training_mode)
                
                
                """
                print("normalized comment unigram: ")
                print(normalized_comment_unigram)
                print("normalized comment bigram: ")
                print(normalized_comment_bigram)
                print("normalized_comment_feature_set_unigram: ")
                print(normalized_comment_feature_set_unigram)
                print("normalized_comment_feature_set_bigram: ")
                print(normalized_comment_feature_set_bigram)
                print("extract_features: ")
                print(normalized_comment_feature_set)
                exit()
                """
                probability_result = classifier.prob_classify(normalized_comment_feature_set)
                
                #Print statistics:
                generate_classifier_data_sets.print_statistics(probability_result, classifier, normalized_comment_feature_set, user_answer, classifier_accuracy)
    #Runtime stamp
    print("Runtime: {}\n".format(datetime.now() - datetime_start))
                