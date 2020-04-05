from colorama import Fore, init, Style
import sys
#Add colours:
init()

#Add command line arguments with describtions:
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--cross_validate', help='Perform a cross validation to the classifier training data with 1/5 split. Input: 0 (Default) = False, 1 = True')
parser.add_argument('--condition_index_dialogue', help='The column number of the condition value in the dialogue CSV file. Default=3')
parser.add_argument('--user_message_index_dialogue', help='The column number of the user message value in the dialogue CSV file. Default=5')
parser.add_argument('--user_id_index_dialogue', help='The column number of the user id value in the dialogue CSV file. Default=1')
parser.add_argument('--user_id_index_prolific', help='The column number of the user ID value in the Prolific CSV file. Default=2')
parser.add_argument('--age_index_prolific', help='The column number of the user age value in the Prolific CSV file. Default=7')
parser.add_argument('--user_sex_index_prolific', help='The column number of the user sex value in the Prolific CSV file. Default=16')
parser.add_argument('--user_student_status_index_prolific', help='The column number of the user student status value in the Prolific CSV file. Default=14')
parser.add_argument('--user_first_language_index_prolific', help='The column number of the user first language information value in the Prolific CSV file. Default=17')
parser.add_argument('--use_bigrams', help='If True, the classifier uses bigrams in feature extraction. Input: True/False. Default=True')
parser.add_argument('--use_stemming', help='If True, stemming process is used in the preprocessing phase. Input: True/False. Default=True')
parser.add_argument('--use_lemma', help='If True, Lemmatization process is used in the preprocessing phase. Input: True/False. Default=False')

args=parser.parse_args()

def check_cmd_arguments():
    '''Check the input values given via command line arguments
    Cross_validate_classifier == 0
    Analysed_text_column_location = -3 (3rd last by default)
    Range of question values to be collected:
    bottom_range = 18 (Default)
    top_range = 40 (Default)
    User-id column number = 8
    '''
    print(Fore.YELLOW)
    try:
        cross_validate = sys.argv[1].split("=")
        cross_validate = cross_validate[1]
        if str(cross_validate) == "1":
            print("Cross validate: True")
            cross_validate = True
        elif str(cross_validate) == "0":
            print("Cross validate: False")
            cross_validate = False
        else:
            print("Cross validate: False (Default)")
            cross_validate == False
    except Exception as e:
        print("e: " + str(e))
        print("Cross validate: False (Default)")
        cross_validate = False 
    
    try:
        condition_index_dialogue = sys.argv[2].split("=")
        condition_index_dialogue = int(condition_index_dialogue[1]) - 1
        print("Bot condition column index in the dialogue CSV file: " + str(condition_index_dialogue + 1))
    except Exception as e:
        print("Bot condition column index in the dialogue CSV file: 3 (Default)")
        condition_index_dialogue = 2
    
    try:
        user_message_index_dialogue = sys.argv[3].split("=")
        user_message_index_dialogue = int(user_message_index_dialogue[1]) - 1
        print("User message column index in the dialogue CSV file: " + str(user_message_index_dialogue + 1))
    except Exception as e:
        print("User message column index in the dialogue CSV file: 5 (Default)")
        user_message_index_dialogue = 4
    
    try:
        user_id_index_dialogue = sys.argv[4].split("=")
        user_id_index_dialogue = int(user_id_index_dialogue[1]) - 1
        print("User id column index in the dialogue CSV file: " + str(user_id_index_dialogue + 1))
    except Exception as e:
        print("User id column index in the dialogue CSV file: 1 (Default)")
        user_id_index_dialogue = 0
    
    try:
        user_id_index_prolific = sys.argv[5].split("=")
        user_id_index_prolific = int(user_id_index_prolific[1]) - 1
        print("User id column number in the Prolific CSV File: " + str(user_id_index_prolific + 1))
    except Exception as e:
        print("User id column number in the Prolific CSV File: 2 (Default)")
        user_id_index_prolific = 1
    
    try:
        age_index_prolific = sys.argv[6].split("=")
        age_index_prolific = int(age_index_prolific[1]) - 1
        print("User age column number in the Prolific CSV File: " + str(age_index_prolific + 1))
    except Exception as e:
        print("User age column number in the Prolific CSV File: 7 (Default)")
        age_index_prolific = 6
    
    try:
        user_sex_index_prolific = sys.argv[7].split("=")
        user_sex_index_prolific = int(user_sex_index_prolific[1]) - 1
        print("User sex column number in the Prolific CSV File: " + str(user_sex_index_prolific + 1))
    except Exception as e:
        print("User sex column number in the Prolific CSV File: 16 (Default)")
        user_sex_index_prolific = 15
    
    try:
        user_student_status_index_prolific = sys.argv[8].split("=")
        user_student_status_index_prolific = int(user_student_status_index_prolific[1]) - 1
        print("User student status column number in the Prolific CSV File: " + str(user_student_status_index_prolific + 1))
    except Exception as e:
        print("User student status column number in the Prolific CSV File: 14 (Default)")
        user_student_status_index_prolific = 13
    
    try:
        user_first_language_index_prolific = sys.argv[9].split("=")
        user_first_language_index_prolific = int(user_first_language_index_prolific[1]) - 1
        print("User first language information column number in the Prolific CSV File: " + str(user_first_language_index_prolific + 1))
    except Exception as e:
        print("User first language information column number in the Prolific CSV File: 17 (Default)")
        user_first_language_index_prolific = 16
        
    try:
        use_bigrams = sys.argv[10].split("=")
        use_bigrams = use_bigrams[1]
        if use_bigrams.lower() == "false":
            use_bigrams = False
            print("Use bigrams in Feature Extraction: " + str(use_bigrams))
        else:
            use_bigrams = True
            print("Use bigrams in Feature Extraction: " + str(use_bigrams))
    except Exception as e:
        print("e: " + str(e))
        print("Use bigrams in Feature Extraction: True (Default)")
        use_bigrams = True
    
    try:
        use_stemming = sys.argv[10].split("=")
        use_stemming = use_stemming[1]
        if use_stemming.lower() == "false":
            use_stemming = False
            print("Use Stemming in Preprocessing: " + str(use_stemming))
        else:
            use_stemming = True
            print("Use Stemming in Preprocessing: " + str(use_stemming))
    except Exception as e:
        print("e: " + str(e))
        print("Use Stemming in Preprocessing: " + str(use_stemming))
        use_stemming = True
    
    try:
        use_lemma = sys.argv[11].split("=")
        use_lemma = use_lemma[1]
        if use_lemma.lower() == "false":
            use_lemma = False
            print("Use Stemming in Preprocessing: " + str(use_lemma))
        else:
            use_lemma = True
            print("Use Stemming in Preprocessing: " + str(use_lemma))
    except Exception as e:
        print("e: " + str(e))
        print("Use Stemming in Preprocessing: " + str(use_lemma))
        use_lemma = True
    
    max_line_count = 9999
    
    print(Style.RESET_ALL)
    
    prolific_column_numbers = []
    prolific_column_numbers.append(user_id_index_prolific)
    prolific_column_numbers.append(age_index_prolific)
    prolific_column_numbers.append(user_sex_index_prolific)
    prolific_column_numbers.append(user_student_status_index_prolific)
    prolific_column_numbers.append(user_first_language_index_prolific)
    
    return cross_validate, user_message_index_dialogue, condition_index_dialogue, user_id_index_dialogue, prolific_column_numbers, max_line_count, use_bigrams, use_stemming, use_lemma
