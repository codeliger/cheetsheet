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

def count_common_pair_words(questions):
    paired_words = list()
    for question in questions:
        if len(question.unique_words) == 0:
            for fwi,first_word in enumerate(question.common_words):
                for swi,second_word in enumerate(question.common_words):
                    if first_word == second_word:
                        continue
                    if length > 0:
                        if (first_word,second_word) in paired_words:
                            paired_words.remove((first_word,second_word))
                    else:
                        paired_words.append((first_word,second_word))


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




if __name__ == '__main__':
    main()
