from bertopic import BERTopic
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
import pandas as pd

def get_words(df):


    sentence_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    hdbscan_model = HDBSCAN(min_cluster_size=30,
                            metric='euclidean',
                            cluster_selection_method='eom',
                            prediction_data=True,
                            min_samples=10)

    topic_model = BERTopic(hdbscan_model=hdbscan_model,
                        embedding_model=sentence_model,
                        language="multilingual",
                        nr_topics=1,
                        calculate_probabilities=True,
                        verbose=True,
                        diversity=0.2,
                        top_n_words=30,
                        n_gram_range=(2, 3))

    topics = df['label_topic'].unique()[1:]

    candidates = df['name_autor'].unique()
    list_word = []

    for candidate in candidates:

        for topic in topics:
            dict_words_cloud = {}
            dict_words_cloud['candidate'] = candidate
            df_temp = df[df['name_autor'] == candidate].reset_index(drop=True)
            text = df_temp[df_temp['label_topic'] ==
                        topic]['tweet_clean'].reset_index(drop=True)
            if len(text) > 10:

                topics, probabilities = topic_model.fit_transform(text)
                list_words_topic = []
                for word, _ in topic_model.get_topic(-1):
                    list_words_topic.append(word)
                dict_words_cloud['topic'] = topic
                dict_words_cloud['words'] = list_words_topic
                list_word.append(dict_words_cloud)
                print(dict_words_cloud)

    df_ = pd.DataFrame(list_word)
    return df_, list_word
