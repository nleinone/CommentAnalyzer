import os
import sys

#REFERENCES:
#https://stackoverflow.com/questions/2081836/reading-specific-lines-only
#https://stackoverflow.com/questions/1767513/read-first-n-lines-of-a-file-in-python

def separate_comments_by_bot_identity(information_collection, keys):
    """Return different bot identities as a list of lists. For example: [happy_bot_comments, happysad_bot_comments, sad_bot_comments, neutral_bot_comments, hello_bot_comments]"""

    bot_id_header = keys[-1]
    discovered_identities = []
    comment_list = []
    identities_list = []
    
    #Search for all the unique bot identities, located last in the comment column
    for comment in information_collection:
        try:
            current_id = comment[bot_id_header]
            if current_id not in discovered_identities:
                discovered_identities.append(current_id)
        except:
            continue
    for id in discovered_identities:
        for comment in information_collection:
            try:
                if comment[bot_id_header] == id:
                    comment_list.append(comment)
            except:
                continue
        identities_list.append(comment_list)
        comment_list = []
        
    #Exclude header row from the comments
    return identities_list[1:], discovered_identities

def distinguish_information(file_line, is_header, keys):
    '''Convert line to dictionary with following keyes: user_name, time, bot_identity, bot_answer, user_answer'''

    file_line_splitted = file_line.split(';')
    dict = {}

    if is_header == 1:

        for index in range(len(file_line_splitted)):
            header = file_line_splitted[index]
            keys.append(header)

        dict = {}
        for index in range(len(keys)):
            dict[keys[index]] = keys[index]

    elif is_header == 2:
        print("descriptive headers")
        #ingore descriptive headers (filter headers)
    else:

        if len(file_line_splitted) == len(keys):
            for index in range(len(keys)):
                dict[keys[index]] = file_line_splitted[index]

    #Bot identity header:
    return dict, keys

def convert_file_to_list(line_count, file_name, number_of_lines_processed):
    '''Add lines in list and return that list. Cannot exceed the max_line_amount (100)'''
    lines_list = []
    counter = 0

    with open('././docs/qualtric_docs/' + file_name) as file:
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
    
def count_remaining_file_lines(file_name, number_of_lines_processed, max_line_count):
    '''Count, return, and print file lines'''
    
    #counter = number_of_lines_processed
    counter = 0
    #print("\n number_of_lines_processed: " + str(number_of_lines_processed))
    #print("\n counter: " + str(counter))
    with open('././docs/qualtric_docs/' + file_name) as file:
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
    '''Fetch csv files from ./docs/prolific_docs/'''

    file_location_prolific = './docs/prolific_docs/'
    file_location_qualtric = './docs/qualtric_docs/'
    
    csv_file_names_prolific = []
    csv_file_names_qualtric = []
    
    file_names_prolific = os.listdir(file_location_prolific)
    file_names_qualtric = os.listdir(file_location_qualtric)
    
    for file_name in file_names_prolific:
        if file_name.endswith((".csv")):
            csv_file_names_prolific.append(file_name)

    for file_name in file_names_qualtric:
        if file_name.endswith((".csv")):
            csv_file_names_qualtric.append(file_name)
            
    return csv_file_names_prolific, csv_file_names_qualtric
