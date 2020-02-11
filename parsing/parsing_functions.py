import os
import sys
def separate_comments_by_bot_identity(information_collection, keys):
    """Return different bot identities as a list of lists. For example: [happy_bot_comments, happysad_bot_comments, sad_bot_comments, neutral_bot_comments, hello_bot_comments]"""

    bot_id_header = keys[-1]
    discovered_id = []
    comment_list = []
    identities_list = []

    #Search for all the unique bot identities, located last in the comment column
    for comment in information_collection:
        try:
            current_id = comment[bot_id_header]
            if current_id not in discovered_id:
                discovered_id.append(current_id)
        except:
            continue
    for id in discovered_id:
        for comment in information_collection:
            try:
                if comment[bot_id_header] == id:
                    comment_list.append(comment)
            except:
                continue
        identities_list.append(comment_list)
        comment_list = []
        
    #Exclude header row from the comments
    return identities_list[1:]

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

def convert_file_to_list(file_count, file_name, number_of_lines_processed, max_line_amount):
    '''Add lines in list and return that list. Cannot exceed the max_line_amount (100)'''
    lines_list = []
    counter = number_of_lines_processed

    with open('././docs/' + file_name) as file:
        file.seek(number_of_lines_processed)
        #data = file.readlines(file_count - number_of_lines_processed)
        for line in file:
            lines_list.append(line)
            #print("line: " + line)
            if counter == file_count:
                #print('Max counter limit exceeded ({})'.format(max_line_amount))
                break
            counter += 1

    file.close()

    return lines_list

def count_remaining_file_lines(file_name, number_of_lines_processed, max_line_count):
    '''Count, return, and print file lines'''

    counter = number_of_lines_processed

    with open('././docs/' + file_name) as file:
        file.seek(number_of_lines_processed)
        #data = file.readlines(max_line_amount)

        for line in file:
            if counter == number_of_lines_processed + max_line_count:
                print('Max counter limit exceeded ({})'.format(max_line_count))
                break
            counter += 1

    file.close()

    return counter

def fetch_document_names():
    '''Fetch csv files from ./docs/'''

    file_location = './docs'
    csv_file_names = []
    file_names = os.listdir(file_location)

    for file_name in file_names:
        if file_name.endswith((".csv")):
            csv_file_names.append(file_name)

    return csv_file_names
