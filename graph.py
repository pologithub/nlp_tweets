from wordcloud import WordCloud
import matplotlib.pyplot as plt


def create_wordcloud(topic_model, topic):
    text = {word: value for word, value in topic_model.get_topic(topic)}
    wc = WordCloud(
        background_color="white",
        max_words=1000,
        font_path='CabinSketch-Bold.ttf',
    )
    wc.generate_from_frequencies(text)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def create_wordcloud_candidat(topic_model, topic):
    text = {word: value for word, value in topic_model.get_topic(topic)}
    wc = WordCloud(
        background_color="white",
        max_words=1000,
        font_path='CabinSketch-Bold.ttf',
    )
    wc.generate_from_frequencies(text)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def wordcloud_plot(column_df):

    text = ' '.join(column_df)

    wc = WordCloud(
        background_color="white",
        max_words=1000,
        font_path='CabinSketch-Bold.ttf',
    )
    wc.generate_from_frequencies(text)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    return plt.show()
