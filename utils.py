import os
import pandas as pd
import tweepy
from prepros import preproc_tweet



def connect_api_twitter():
    import tweepy
    # bearer_token = bearer_token = "AAAAAAAAAAAAAAAAAAAAALxaaAEAAAAAJsf9AT1gAYdiWmKF37Q5nCcrR%2F8%3DWpHCL0jYWPK84ud6cYrcgzMSvu1wqkpXuiBrNiVD97ZawEMOtZ"
    bearer_token = bearer_token = "AAAAAAAAAAAAAAAAAAAAAER1aAEAAAAAxNYjEUf%2F96Lgqe5JYYfxPFHbX6E%3DrDVrBvaPGDE2RHBZeNr9A6rwOhK9ULmal5TvOI1fzUdBxqKdCX"
    client = tweepy.Client(bearer_token=bearer_token)
    return client


def get_the_last_tweet():

    list_candidats = [{
        'name': 'Anne Hidalgo',
        'id': '26073581'
    }, {
        'name': 'jean-luc mélenchon',
        'id': '80820758'
    }, {
        'name': 'Emmanuel Macron',
        'id': '1976143068'
    }, {
        'name': 'Marine Le Pen',
        'id': '217749896'
    }, {
        'name': 'Eric Zemmour',
        'id': '1183418538285027329'
    }, {
        'name': 'Valérie Pécresse',
        'id': '49969223'
    }, {
        'name': 'Philippe Poutou',
        'id': '374392774'
    }, {
        'name': 'Nathalie Arthaud',
        'id': '1003575248'
    }, {
        'name': 'Yannick Jadot',
        'id': '117761523'
    }, {
        'name': 'N. Dupont-Aignan',
        'id': '38170599'
    }, {
        'name': 'Jean Lassalle',
        'id': '102722347'
    }, {
        'name': 'Fabien Roussel',
        'id': '1324449588'
    }]

    file = 'tweets_with_labels.csv'
    path_file = os.path.abspath(os.path.join(os.getcwd(), 'data', file))
    df = pd.read_csv(path_file)

    list_last_tweet = []
    for index, candidate in enumerate(list_candidats):
        dict_last_tweet = {}
        id = candidate['id']
        name = candidate['name']
        last_tweet = df[df['id_autor'] == int(id)]['id_tweet'].max()
        dict_last_tweet['name'] = name
        dict_last_tweet['id_candidat'] = id
        dict_last_tweet['id_last_tweet'] = last_tweet
        list_last_tweet.append(dict_last_tweet)
    return list_last_tweet




def get_last_tweet_api():

    last_tweet = get_the_last_tweet()
    df = pd.DataFrame()
    list_tweet = []
    client = connect_api_twitter()
    print(client)
    for index, candidate in enumerate(last_tweet):
        id = candidate['id_candidat']
        name = candidate['name']
        since_id = candidate['id_last_tweet']
        token = None

        tweets = client.get_users_tweets(
            id=int(id),
            since_id=since_id,
            tweet_fields=[
                'attachments', 'author_id', 'context_annotations',
                'conversation_id', 'created_at', 'entities', 'geo', 'id',
                'in_reply_to_user_id', 'lang', 'possibly_sensitive',
                'referenced_tweets', 'reply_settings', 'source', 'text',
                'withheld', 'public_metrics'
            ],
            max_results=100)

        index_2 = 0

        # test_token = tweets.meta.get('next_token') is not None

        while (tweets.meta.get('next_token') is not None) | (index_2 == 0):
            if index_2 == 0:
                token = None

            if index_2 != 0:
                token = tweets.meta.get('next_token')

            tweets = client.get_users_tweets(
                id=int(id),
                since_id=since_id,
                tweet_fields=[
                    'attachments', 'author_id', 'context_annotations',
                    'conversation_id', 'created_at', 'entities', 'geo', 'id',
                    'in_reply_to_user_id', 'lang', 'possibly_sensitive',
                    'referenced_tweets', 'reply_settings', 'source', 'text',
                    'withheld', 'public_metrics'
                ],
                max_results=100,
                pagination_token=token)
            if tweets.data:
                for tweet in tweets.data:
                    dict_tweet = {}
                    dict_tweet['id_autor'] = id
                    dict_tweet['name_autor'] = name
                    dict_tweet['id_tweet'] = tweet['id']
                    dict_tweet['tweet'] = tweet['text']
                    dict_tweet['date_tweet'] = tweet['created_at']
                    if tweet['referenced_tweets']:
                        dict_tweet['referenced_tweets_id'] = str(
                            tweet['referenced_tweets'][0].get('id'))
                        dict_tweet['referenced_tweets_type'] = str(
                            tweet['referenced_tweets'][0].get('type'))
                    dict_tweet['possibly_sensitive'] = tweet['possibly_sensitive']
                    dict_tweet['in_reply_to_user_id'] = tweet[
                        'in_reply_to_user_id']
                    dict_tweet['conversation_id'] = tweet['conversation_id']
                    dict_tweet['source'] = tweet['source']
                    dict_tweet['context_annotations'] = tweet[
                        'context_annotations']
                    dict_tweet['entities'] = tweet['entities']
                    dict_tweet['retweet_count'] = tweet['public_metrics'][
                        'retweet_count']
                    dict_tweet['reply_count'] = tweet['public_metrics'][
                        'reply_count']
                    dict_tweet['like_count'] = tweet['public_metrics'][
                        'like_count']
                    dict_tweet['quote_count'] = tweet['public_metrics'][
                        'quote_count']
                    if dict_tweet['entities']:
                        if tweet['entities'].get('mentions'):
                            list_mentions = []
                            for mention in tweet['entities'].get('mentions'):
                                list_mentions.append(mention['username'])
                            dict_tweet['mentions'] = list_mentions
                        if tweet['entities'].get('hashtags'):
                            list_tag = []
                            for tag in tweet['entities'].get('hashtags'):
                                list_tag.append(tag['tag'])
                            dict_tweet['hashtags'] = list_tag

                    list_tweet.append(dict_tweet)

                index_2 += 1

    df = pd.DataFrame(list_tweet)
    df = df[df['referenced_tweets_type'].isnull()]
    return df


def add_new_tweet_to_csv(df_tweet_with_labels, df_new_tweet_preproc):
    df_ = pd.concat([df_tweet_with_labels, df_new_tweet_preproc])
    file = 'tweets_with_labels.csv'
    path_file = os.path.abspath(os.path.join(os.getcwd(), 'data', file))
    df_.to_csv(path_file, index=False)


def get_topic_prediction(df_new_tweet, model):
    from bertopic import BERTopic
    df_new_tweet_preproc = preproc_tweet(df_new_tweet)

    df_new_tweet_preproc['prediction'] = df_new_tweet_preproc[
        'tweet_clean'].apply(lambda x: model.transform(x)[0][0])

    df_topics_name = pd.read_csv(os.path.abspath(os.path.join(os.getcwd(),'data', 'df_topics_name.csv')))
    dico = dict(zip(df_topics_name['Topic'], df_topics_name['label_name']))
    df_new_tweet_preproc['prediction_name'] = df_new_tweet_preproc['prediction'].map(dico)
    return df_new_tweet_preproc['prediction_name']
