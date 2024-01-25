import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

df = pd.read_csv('./naver_news_titles_20240125.csv')
print(df.head())
df.info()

X = df['titles']
Y = df['category']

label_encoder = LabelEncoder()
labeled_y = label_encoder.fit_transform(Y)
print(labeled_y[:3])
label = label_encoder.classes_
print(label)

# pickle은 파이썬의 데이터 형태를 그대로 저장해온다. 피클 처럼 그대로 저장한다 이런뜻으로 유래?
# 클래스 그대로 저장하고 그대로 불러온다.

with open('./models/label_encoder.pickle', 'wb') as f:
    pickle.dump(label_encoder, f)

onehot_y = to_categorical(labeled_y)
# print(onehot_y[:3])

okt = Okt()
for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
    # okt -> 형태소 분리, 하지만 완벽하게 동작하지는 않음.
    # stem = True -> 원형으로 바꾸어줌 ex) 말씀드렸다 -> 말씀드리다
    #  등장한 -> 등장하다로 바꾸어야하는데 등장, 한 으로 나누는등의 문제발생
    # -> 가급적 한 글자짜리는 제외하는게 나음.
    # + 감탄사나 접속사들은 없애는게 나음. 그리고, 등
    # stopword.csv참조 -> 불용어(어학쪽에서 쓰이는 의미랑은 조금 다름, 학습에 도움이 되지않는 단어들)

# print(X[1:5])

stopwords = pd.read_csv('./stopwords.csv', index_col=0)

for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)
# print(X[0])
#
token = Tokenizer()
token.fit_on_texts(X)
tokened_x = token.texts_to_sequences(X)
wordsize = len(token.word_index) + 1
# print(tokened_x)
# print(wordsize)

with open('./models/news_token.pickle','wb') as f:
    pickle.dump(token,f)

max = 0
for i in range(len(tokened_x)):
    if max < len(tokened_x[i]):
        max = len(tokened_x[i])

print(max)
x_pad = pad_sequences(tokened_x, max)
print(x_pad)

X_train, X_test, Y_train, Y_test = train_test_split(
    x_pad, onehot_y, test_size=0.2)
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)
xy = X_train, X_test, Y_train, Y_test
xy = np.array(xy, dtype=object)
np.save('./news_data_max_{}_wordsize_{}'.format(max, wordsize), xy)
# for j in range(len(X)):
#     words = []
#     for i in range(len(X[j])):
#         if len(X[j][i]) > 1:
#             if X[j][i] not in list(stopwords['stopword']):
#                 words.append(X[j][i])
#     X[j] = ' '.join(words)
# # print(X[0])
#
# token = Tokenizer()
# token.fit_on_texts(X)
# tokened_x = token.texts_to_sequences(X)
# wordsize = len(token.word_index) + 1
# print(tokened_x[0:3])
# print(wordsize)
#
# with open('./models/news_token.pickle', 'wb') as f:
#     pickle.dump(token, f)
#
# max = 0
# for i in range(len(tokened_x)):
#     if max < len(tokened_x[i]):
#         max = len(tokened_x[i])
# print(max)
#
# x_pad = pad_sequences(tokened_x, max)
# print(x_pad[:3])
#
# X_train, X_test, Y_train, Y_test = train_test_split(
#     x_pad, onehot_y, test_size=0.2)
# print(X_train.shape, Y_train.shape)
# print(X_test.shape, Y_test.shape)
#
# xy = X_train, X_test, Y_train, Y_test
# np.save('./crawling_data/news_data_max_{}_wordsize_{}'.format(max, wordsize), xy)
#
#
#
#
