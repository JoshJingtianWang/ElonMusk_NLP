import pickle
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import NMF, TruncatedSVD
import pandas as pd

#load saved tweet df
with open(r"tweets_df_en.pkl", "rb") as input_file:
    tweets_df_en = pickle.load(input_file)
	
# # My custom list of stop words.
stop_list = ["Elon", "Musk", "Twitter", 'elon', 'musk', 'twitter', 'url', 'URL', 'ElonMusk', 'elonmusk']
# # Updates spaCy's default stop words list with my additional words. 
nlp.Defaults.stop_words.update(stop_list)

# Iterates over the words in the stop words list and resets the "is_stop" flag.
for word in STOP_WORDS:
    lexeme = nlp.vocab[word]
    lexeme.is_stop = True
   
#remove stop word, lemmatization
def preprocess(doc):
    sent_cleaned = ''
    for token in nlp(doc):
        if not token.is_stop:
            if not token.pos_ == 'PUNCT':
                sent_cleaned += token.lemma_.lower()
                sent_cleaned += ' '
    sent_cleaned = sent_cleaned.strip()
    return sent_cleaned
    
processed = tweets_df_en['CleanedText'].\
        map(lambda x: preprocess(x))

print("Preprocessing done.")
    
#TF-IDF
tv = TfidfVectorizer(stop_words=None, ngram_range=(1,2))
tv_out = tv.fit_transform(processed)
tfidf = pd.DataFrame(tv_out.toarray(), columns=tv.get_feature_names())

print("TF-IDF done.")

#NMF
nmf = NMF(4, init = "nndsvda")
nmf.fit(tfidf)

print("NMF done.")

#saving fitted nmf
with open('nmf.pkl', 'wb') as handle:
    pickle.dump(nmf, handle, protocol=pickle.HIGHEST_PROTOCOL)