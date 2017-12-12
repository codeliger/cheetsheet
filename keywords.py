import re
import sys
import typing

class Question:
    def __init__(self,question,answer,words):
        self.question = question
        self.answer = answer
        self.words = words
        self.unique_words = list()
        self.common_words = list()
        self.describing_words = list()

def create_questions_from_text(csv_text):
    word_regex = re.compile('\s?(\w+)\s?')
    list_of_pairs = csv_text.split('\n')
    questions = list()
    for pair in list_of_pairs:
        question_and_answer = pair.split(',')
        question = question_and_answer[0].lower()
        question_answer = question_and_answer[1].lower()
        question_words = word_regex.findall(question)
        question_object = Question(question,question_answer,question_words)
        questions.append(question_object)
    return questions

def count_all_words(questions):
    words = dict()
    for question in questions:
        for word in question.words:
            if word in words:
                words[word] += 1
            else:
                words[word] = 1
    return words

# create a list with every possible word pair for every commonly used word
def list_common_pair_words(questions):
    paired_words = dict()
    for question in questions:
        if len(question.unique_words) == 0:
            for fwi,first_word in enumerate(question.common_words):
                for swi,second_word in enumerate(question.common_words):
                    if fwi == swi: # skip if indexes match
                        continue
                    if (first_word,second_word) in paired_words:
                        paired_words[(first_word,second_word)] +=1
                    else:
                        paired_words[(first_word,second_word)] = 1
    print(len(paired_words),'paired words.')
    # print(sorted(paired_words.values(),reverse=True))
    return paired_words
    
# remove all common pairs that repeat because more than one question must have them
def filter_common_pair_words(common_pairs):
    # edge case if [1,2] and [2,1] exist delete them all
    unique_pairs =  [common_pair for common_pair in common_pairs if common_pairs[common_pair] == 1]
    # print(len(unique_pairs))    
    # temp_pairs = list(unique_pairs)
    # for ai,pair_a in enumerate(temp_pairs):
    #     for bi,pair_b in enumerate(temp_pairs):
    #         # if the reversed tuple is equal to another tuple
    #         if ai==bi:
    #             continue
    #         # print("Comparing:",pair_a[::-1],pair_b)
    #         if pair_a[::-1] == pair_b:
    #             unique_pairs.remove(pair_b)
    # print(len(unique_pairs))
    # exit()
    return unique_pairs
                


def assign_describing_words_to_non_unique_questions(questions,unique_pairs):
    temp_pairs = list(unique_pairs)
    for question in questions:
        for unique_pair in unique_pairs:
            if len(question.unique_words) == 0:
                if unique_pair[0] in question.words and unique_pair[1] in question.words:
                    if unique_pair in temp_pairs:
                        question.describing_words.append(unique_pair)
                        temp_pairs.remove(unique_pair)
                        break

def assign_unique_describing_word_to_questions(questions):
    for question in questions:
        if len(question.unique_words) > 0:
            question.describing_words.append(question.unique_words[0])

def count_questions_without_describing_words(questions):
    print("=== Questions without describing words:")
    for question in questions:
        if len(question.describing_words) == 0:
            print(question.question)

def filter_unique_words(words):
    return [word for word in words if words[word] == 1]

def filter_common_words(words):
    return [word for word in words if words[word] > 1]

def set_question_words(questions:list,unique_words,common_words):
    for question in questions:
        for word in question.words:
            if word in unique_words:
                question.unique_words.append(word)
            elif word in common_words:
                question.common_words.append(word)

def count_all_question_words(questions,words):
    common = 0
    unique = 0
    for question in questions:
        common += len(question.common_words)
        unique += len(question.unique_words)
    word_count = 0
    for word in words:
        word_count += words[word]
    return common,unique,word_count

def print_question_results(questions):
    for question in questions:
        print(question.describing_words,question.answer,question.question)
        print()

def main():
    with open('questions.csv','r',encoding='utf-8') as file:
        csv_text = file.read().replace('?','').replace("'",'').replace('/',' or ')
    questions = create_questions_from_text(csv_text)
    words = count_all_words(questions)
    unique_words = filter_unique_words(words)
    common_words = filter_common_words(words)
    set_question_words(questions,unique_words,common_words)
    common,unique,word_count = count_all_question_words(questions,words)
    print(common,unique,common+unique,word_count)
    common_pairs = list_common_pair_words(questions)
    unique_pairs = filter_common_pair_words(common_pairs)
    assign_describing_words_to_non_unique_questions(questions,unique_pairs)
    assign_unique_describing_word_to_questions(questions)
    count_questions_without_describing_words(questions)
    print_question_results(questions)

if __name__ == '__main__':
    main()
