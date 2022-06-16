from bertopic import BERTopic
from google.cloud import storage

def create_model():
    from bertopic import BERTopic
    from hdbscan import HDBSCAN
    from sentence_transformers import SentenceTransformer

    sentence_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    hdbscan_model = HDBSCAN(min_cluster_size=30,
                            metric='euclidean',
                            cluster_selection_method='eom',
                            prediction_data=True,
                            cluster_selection_epsilon=0.12,
                            min_samples=5)

    topic_model = BERTopic(hdbscan_model=hdbscan_model,
                        embedding_model=sentence_model,
                        language="multilingual",
                        nr_topics=20,
                        calculate_probabilities=True,
                        verbose=True,
                        diversity=0.4,
                        n_gram_range=(1, 3))

    return topic_model


def get_model_from_local():
    import os
    from bertopic import BERTopic
    path_to_model = os.path.abspath(
        os.path.join(os.getcwd(), 'data', "model_bertopic"))
    trained_model = BERTopic.load(path_to_model)
    return trained_model


def get_model_from_gcp(local=False, **kwargs):
    """method to get the training data (or a portion of it) from google cloud bucket"""
    # Add Client() here
    BUCKET_NAME = "mrspresident"
    BUCKET_MODEL_NAME =  "model_bertopic"
    client = storage.Client()
    if local:
        path = "data/model_bertopic"
    else:

        # path = "gs://{}/{}".format(BUCKET_NAME, BUCKET_TRAIN_DATA_PATH)

        model = "gs://{}/{}".format(BUCKET_NAME, BUCKET_MODEL_NAME)

        # path = "s3://wagon-public-datasets/taxi-fare-train.csv"

    return model
