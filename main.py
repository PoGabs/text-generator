from nltk.tokenize import WhitespaceTokenizer
from nltk.util import bigrams
from collections import Counter
import random
import string


corpus_file_name_user_input = input()
corpus_file_handle = open(corpus_file_name_user_input, "r", encoding="utf-8")
corpus = corpus_file_handle.read()
tokenized = WhitespaceTokenizer()
tk = tokenized.tokenize(corpus)
all_tokens = len(tk)
unique_tokens = len(set(tk))
bigram_list = list(bigrams(tk))
corpus_file_handle.close()
index_dict = {}
count_dict = {}
for head, tail in bigram_list:
    index_dict.setdefault(head, []).append(tail)
for key, values in index_dict.items():
    count_dict[key] = Counter(values)
sentences = []
outer_counter = 0
while outer_counter < 10:
    sentence = []
    inner_counter = 0
    max_inner = random.randint(5, 15)
    while inner_counter < max_inner:
        if len(sentence) > 4 and sentence[-1][-1] in ".?!":
            break
        if inner_counter == max_inner - 1:
            current_word = sentence[-1]
            feed_this = count_dict[current_word].most_common()
            word_list = []
            weight_list = []
            for i in feed_this:
                word_list.append(i[0])
                weight_list.append(i[1])
            found = False
            for word in word_list:
                if word[-1] == ".":
                    found = True
            if not found:
                outer_counter = outer_counter - 1
                sentence = []
                break
            random_ = random.choices(word_list, weight_list)[0]
            if random_[-1] != ".":
                continue
            sentence.append(random_)
            inner_counter += 1
            continue
        if inner_counter > 1:
            current_word = sentence[-1]
            feed_this = count_dict[current_word].most_common()
            word_list = []
            weight_list = []
            for i in feed_this:
                word_list.append(i[0])
                weight_list.append(i[1])
            random_ = random.choices(word_list, weight_list)[0]
            sentence.append(random_)
            inner_counter += 1
            continue
        first_word = random.choices(list(count_dict.keys()))[0]
        if first_word[0] in string.ascii_lowercase or first_word[-1] in string.punctuation or first_word[0] in string.punctuation or first_word[0] in string.digits:
            continue
        feed_this = count_dict[first_word].most_common()
        word_list = []
        weight_list = []
        for i in feed_this:
            word_list.append(i[0])
            weight_list.append(i[1])
        first_random = random.choices(word_list, weight_list)[0]
        sentence.append(first_word)
        sentence.append(first_random)
        inner_counter += 1
    if len(sentence) > 0:
        sentences.append(sentence)
    outer_counter += 1
for sentence in sentences:
    print(" ".join(sentence))
