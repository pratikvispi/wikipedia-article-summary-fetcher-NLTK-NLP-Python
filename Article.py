import bs4 as bs
import urllib.request
import re
import nltk
import heapq

scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Natural_language_processing')

article = scraped_data.read()

parsed = bs.BeautifulSoup(article,'lxml')

para = parsed.find_all('p')

text = ""

for p in para:
    text += p.text


text = re.sub(r'\[[0-9]*\]' , ' ',text)
text = re.sub(r'\s+' , ' ' , text)

formatted_text = re.sub('[a-zA-Z]' , ' ' , text)
formatted_text = re.sub(r'\s+', ' ' , formatted_text)

sentence_list = nltk.sent_tokenize(text)

# print(sentence_list)

stop_words = nltk.corpus.stopwords.words('english')
# print(stop_words)

frequencies = {}

for word in nltk.word_tokenize(formatted_text):
    if word not in stop_words:
        if word not in frequencies.keys():
            frequencies[word] = 1
        else:
            frequencies[word] += 1

max_frequency = max(frequencies.values())

for word in frequencies.keys():
    frequencies[word] = (frequencies[word] / max_frequency)

sentence_score = {}
for sentence in sentence_list:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in frequencies.keys():
            if len(sentence.split(' ')) < 30:
                if sentence not in sentence_score.keys():
                    sentence_score[sentence] = frequencies[word]
                else:
                    sentence_score[sentence] += frequencies[word]

# print(sentence_score)

fetch_summary = heapq.nlargest(10 , sentence_score , key = sentence_score.get)

final_summary = ' '.join(fetch_summary)

print(final_summary)