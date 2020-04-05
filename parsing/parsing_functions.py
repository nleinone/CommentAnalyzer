import os
import sys

#REFERENCES:
#https://stackoverflow.com/questions/2081836/reading-specific-lines-only
#https://stackoverflow.com/questions/1767513/read-first-n-lines-of-a-file-in-python

def extract_user_ids(information_collection, user_id_index_dialogue, keys):
    '''Extract all user ids from the dialogue docs file (csv)'''
    
    user_ids = []
    
    user_id_header = keys[user_id_index_dialogue]
    
    for comment in information_collection:
        try:
            #print("\n comment: " + str(comment))
            user_ids.append(comment[user_id_header])
        except Exception as e:
            continue
    user_ids = list(dict.fromkeys(user_ids))
    
    #print("\n user_ids: " + str(user_ids))
    return user_ids

def parse_relevant_comments(information_collection, user_id_index_dialogue, keys, user_id_collection):
    '''Parses the relevant comments from the dialogue data file'''
    #Time stamp location
    #user id location
    #print("\ninformation_collection: " + str(information_collection))
    
    user_id_header = keys[user_id_index_dialogue]
    
    #timestamps = []
    relevant_information = []
    gathered_comments = []
    
    counter = 0
    #print("\n user_id_collection: " + str(user_id_collection))
    #print("\n information_collection: " + str(len(information_collection)))
    
    #print("\n information_collection: " + str(information_collection[0]))
    
    #print("\n user_id_collection: " + str(len(user_id_collection)))
    #print("\n information_collection: " + str(len(information_collection)))

    for user_id in user_id_collection[1:]:
        for comment in information_collection[1:]:
            #print("\n comment[user_id_header]: " + str(comment[user_id_header]))
            #print("\n user_id: " + str(user_id))
            #print("\n comment: " + str(comment))
            #try:
            if comment[user_id_header] == user_id:
                if len(comment.keys()) ==  len(keys):
                    gathered_comments.append(comment)
                    #print("\n comment to gathered_comments: " + str(comment))
                #print("\n comment to gathered_comments len: " + str(len(comment.keys())))
            #except KeyError as e:
                #print(e)
                #pass
        
        #print("\n gathered_comments: " + str(gathered_comments))
        relevant_information.append(gathered_comments[-1])
        #print("\n gathered_comments [-1]: " + str(gathered_comments[-1]))
        gathered_comments = []
    #print("\n relevant_information: " + str(relevant_information))
    #print("\n relevant_information len: " + str(len(relevant_information)))
    print("\n relevant_information: " + str(len(relevant_information)))
    return relevant_information

def separate_comments_by_condition(information_collection, keys, condition_index_dialogue, user_id_index_dialogue):
    """Return different bot identities as a list of lists. For example: [happy_bot_comments, happysad_bot_comments, sad_bot_comments, neutral_bot_comments, hello_bot_comments]"""
    
    #print("\nkeys: " + str(keys))
    #print("\ncondition_index_dialogue: " + str(condition_index_dialogue))
    
    condition_header = keys[condition_index_dialogue]
    discovered_conditions = []
    comments_by_condition_list = []
    conditions_list = []
    user_ids = {}
    
    comment_list = []
    
    
    #print("\n information_collection1: " + str(len(information_collection)))
    #Parse only the last dialogue data:
    user_id_collection = extract_user_ids(information_collection, user_id_index_dialogue, keys)
    relevant_information = parse_relevant_comments(information_collection, user_id_index_dialogue, keys, user_id_collection)
    
    #print("\n relevant_information1: " + str(len(relevant_information)))
    
    #sys.exit()
    
    #Search for all the unique bot identities
    for comment in relevant_information:
        try:
            current_condition = comment[condition_header]
            if current_condition not in discovered_conditions:
                discovered_conditions.append(current_condition)
        except:
            continue

    for condition in discovered_conditions:
        for comment in relevant_information:
            try:
                
                if comment[condition_header] == condition:
                    #print("\ncomment[condition_header]: " + str(comment[condition_header]))
                    comment_list.append(comment)
            except:
                continue
        comments_by_condition_list.append(comment_list)
        comment_list = []
        
    #Exclude header row from the comments
    #print("\ncomments_by_condition_list: " + str(len(comments_by_condition_list)))
    #sys.exit()
    return comments_by_condition_list, discovered_conditions

def clean_up_dictionaries(information_dictionary, keys):
    '''Clean up unecessary keys left by the parser'''
    
    if "" in information_dictionary:
        del information_dictionary[""]
    if "," in information_dictionary:
        del information_dictionary[","]
    if "\n" in information_dictionary:
        del information_dictionary["\n"]
        
        
    for item in keys:
        if len(item) < 2:
            #print(item)
            keys.remove(item)
        
    return information_dictionary, keys
    
def distinguish_information(file_line, is_header, keys):
    '''Convert line to dictionary with following keyes: user_name, time, bot_identity, bot_answer, user_answer'''
    #print("\nLine: " + str(file_line))
    file_line_splitted = file_line.split('"')
    #print("\nfile_line_splitted: " + str(file_line_splitted))
    information_dictionary = {}
    
    d, file_line_splitted = clean_up_dictionaries({}, file_line_splitted)
    
    #print("\nfile_line_splitted: " + str(file_line_splitted))
    
    if is_header == 1:

        for index in range(len(file_line_splitted)):
            header = file_line_splitted[index]
            keys.append(header)

        information_dictionary = {}
        for index in range(len(keys)):
            information_dictionary[keys[index]] = keys[index]

    else:
        #if len(file_line_splitted) == len(keys):
        #try:
        for index in range(len(keys)):
            information_dictionary[keys[index]] = file_line_splitted[index]
        #except IndexError as e:
            #print(e)
            #pass
    #Clean up the word dictionary:
    information_dictionary, keys = clean_up_dictionaries(information_dictionary, keys)
    
    
    
    return information_dictionary, keys

def convert_file_to_list(line_count, file_name, number_of_lines_processed):
    '''Add lines in list and return that list. Cannot exceed the max_line_amount (100)'''
    lines_list = []
    counter = 0

    with open('././docs/dialogue_docs/' + file_name) as file:
        file.seek(number_of_lines_processed)
        for i in range(line_count):
            try:
                line = next(file)
                lines_list.append(line)
                counter += 1
            except Exception as e:
                file.close()
                print("Error: " + str(e))
                return lines_list
        #data = file.readlines(file_count - number_of_lines_processed)
        #for line in file:
            #lines_list.append(line)
            #print("line: " + line)
            #if counter == line_count:
                #print('Max counter limit exceeded ({})'.format(max_line_amount))
                #break
            #counter += 1

    file.close()
    return lines_list

def file_line_counter(file):
    counter = 0
    for line in file:
        counter += 1
    #print("total line count: " + str(counter))
    
def count_remaining_file_lines(file_name, number_of_lines_processed, max_line_count):
    '''Count, return, and print file lines'''
    
    #counter = number_of_lines_processed
    counter = 0
    #print("\n number_of_lines_processed: " + str(number_of_lines_processed))
    #print("\n counter: " + str(counter))
    with open('././docs/dialogue_docs/' + file_name) as file:
        file.seek(number_of_lines_processed)
        for i in range(max_line_count):
            try:
                #print(str(i))
                line = next(file)
                counter += 1
                #print("\n" + line)
                #print("Counter: " + str(counter))
                #file.seek(number_of_lines_processed) #Seek 0
                #line = file.readline()
                #print("\n line " + str(i) + ":" + " " + str(line))
            except Exception as e:
                file.close()
                #print("Error: " + str(e))
                return counter
            #data = file.readlines(max_line_amount)
            
            #for line in file:
                #print("\n line " + str(counter) + ":" + " " + str(line))
                #if counter == max_line_count:
                    #print('Max counter limit exceeded ({})'.format(max_line_count))
                    #break
    
    
    #print("\n count_remaining_file_lines: counter: " + str(counter))
    return counter

def fetch_document_names():
    '''Fetch csv files from all the document folders inside /docs/'''

    file_location_prolific = './docs/prolific_docs/'
    file_location_qualtric = './docs/qualtric_docs/'
    file_location_dialogue = './docs/dialogue_docs/'
    
    csv_file_names_prolific = []
    csv_file_names_qualtric = []
    csv_file_names_dialogue = []
    
    file_names_prolific = os.listdir(file_location_prolific)
    file_names_qualtric = os.listdir(file_location_qualtric)
    file_names_dialogue = os.listdir(file_location_dialogue)
    
    for file_name in file_names_prolific:
        if file_name.endswith((".csv")):
            csv_file_names_prolific.append(file_name)

    for file_name in file_names_qualtric:
        if file_name.endswith((".csv")):
            csv_file_names_qualtric.append(file_name)
    
    for file_name in file_names_dialogue:
        if file_name.endswith((".csv")):
            csv_file_names_dialogue.append(file_name)
    
    return csv_file_names_qualtric, csv_file_names_prolific, csv_file_names_dialogue
