# CommentAnalyzer
Computer Science and Engineering Master's Thesis Implementation by Niko Leinonen

Description:

This analysis pipeline tool extracts and parses natural language processing information from chatbot dialogue data and user information from the related Prolific platform export file. More specific description can be seen in the master thesis work.

Abstract from the thesis:

This thesis introduces an analysis pipeline tool with capabilities of NLPinformation extraction from Customer-Chatbot interaction dialoguedata and user information parsing using the Prolific platform exportfiles. The functionalities of the analysis pipeline tool are evaluated withtwo separate test setups, one of them using real users and another usingemulated data, derived from Amazon mobile device reviews. Besidesthe implementation work, the thesis introduces different state-of-artNatural Language Processing methods and techniques and describesdifferent chatbots implemented in the past and in the modern times,giving insight to a current state of Natural Language Processingresearch and chatbot development.  This master’s thesis is done incollaboration with The Center of Ubicomp and Oulu Business School.

Operation:

There are two version of the system, which can be downloaded from the two separate branches of this repository: pilot_version and master.

The system can be ran with its default values, but if changes are needed, here is the CLI spell for running the master version of the program:

python main.py --cross_validate=1 --condition_index_dialogue=3 --user_message_index_dialogue=5 --user_id_index_dialogue=1 --user_id_index_prolific=2 --age_index_prolific=7 --user_sex_index_prolific=16 --user_student_status_index_prolific=14 --user_first_language_index_prolific=17 --use_bigrams=False

You can see the argument information with the following command: python main.py --h

The source code contains also interesting and useful links to various different sources, which were studied while developing this system.
