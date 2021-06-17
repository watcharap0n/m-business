from db import MongoDB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from pythainlp.tokenize import word_tokenize
import os

client = os.environ.get('MONGODB_URI')
# client = 'mongodb://127.0.0.1:27017'
db = MongoDB(database_name='Mango', uri=client)
collection = 'intents'


def intent_model(p_text=str, query=str):
    data = db.find(collection=collection, query={'access_token': query})
    data = list(data)
    sum_text = []
    ans_text = [x['answer'] for x in data]
    embedding = [x for x in range(len(ans_text))]
    for text in data:
        txt = ''
        for v in text['question']:
            txt += v
        sum_text.append(txt)

    count_vector = CountVectorizer(tokenizer=word_tokenize)
    tf_transformer = TfidfTransformer(use_idf=False)
    x_train_count = count_vector.fit_transform(sum_text)
    tf_transformer.fit(x_train_count)
    x_train_tf = tf_transformer.transform(x_train_count)
    my_classifier = LogisticRegression(penalty='none')
    my_classifier.fit(x_train_tf, embedding)
    x_test_count = count_vector.transform([p_text])
    x_test_tf = tf_transformer.transform(x_test_count)

    prediction = my_classifier.predict(x_test_tf)
    proba = my_classifier.predict_proba(x_test_tf)[0][prediction]
    return {'predict': prediction, 'confident': proba, 'answers': ans_text}
