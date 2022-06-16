import pandas as pd
import re



def split_count(text):
    """emoji function return list of emoji and text without emoji"""
    import emoji
    import regex
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI['en'] for char in word):
            emoji_list.append(word)

    for emo in emoji_list:
        text = text.replace(emo, '')

    return emoji_list, text



def remove_stop_word(text):
    """function to remove stop words"""
    from nltk.corpus import stopwords
    final_stopwords_list = stopwords.words('english') + stopwords.words(
        'french')
    text = [w for w in text.split() if not w in final_stopwords_list]
    return ' '.join(text)


def preproc_tweet(df):
    """ cleaning function"""
    # remove @ and the word or name attached


    df['tweet_clean'] = df['tweet'].apply(
        lambda row: " ".join(filter(lambda x: x[0] != "@", row.split())), 1)

    # remove web site link


    df['tweet_clean'] = df['tweet_clean'].apply(
        lambda row: re.sub(r"http\S+", "", row).lower(), 1)


    # remove # and the word or name attached


    df['tweet_clean'] = df['tweet_clean'].apply(
        lambda row: " ".join(filter(lambda x: x[0] != "#", row.split())), 1)


    df['emoji'] = df['tweet_clean'].apply(
        lambda x: ' '.join(emoji for emoji in split_count(x)[0]))


    df['tweet_clean'] = df['tweet_clean'].apply(
        lambda x: ''.join(emoji for emoji in split_count(x)[1]))


    df['tweet_clean'] = df['tweet_clean'].apply(
        lambda x: ''.join(word for word in x if not word.isdigit()))


    df['tweet_clean'] = df['tweet_clean'].apply(lambda x: remove_stop_word(x))

    df['tweet_clean'] = df['tweet_clean'].apply(
        lambda x: x.replace('france', ''))

    df['tweet_clean'] = df['tweet_clean'].apply(
        lambda x: x.replace('gauche', ''))

    # Keep only tweet

    df = df[df['referenced_tweets_type'].isnull()]

    df = df.reset_index(drop=True)

    return df
