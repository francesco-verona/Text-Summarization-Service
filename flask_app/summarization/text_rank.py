import nltk
import numpy as np
import networkx as nx
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

nltk.download("punkt")
nltk.download("stopwords")

def textrank_summarize(text, top_n=3):
    # 1) Split in frasi
    sentences = sent_tokenize(text)
    
    # 2) Preprocessing: lowercase e rimozione stopwords
    stop_words = set(stopwords.words('italian'))
    clean_sentences = []
    for sent in sentences:
        words = [w.lower() for w in word_tokenize(sent) if w.isalpha()]
        filtered = [w for w in words if w not in stop_words]
        clean_sentences.append(" ".join(filtered))
    
    # 3) Costruzione matrice di similarità
    vectorizer = CountVectorizer().fit_transform(clean_sentences)
    sim_matrix = cosine_similarity(vectorizer)
    
    # 4) Grafo e PageRank
    nx_graph = nx.from_numpy_array(sim_matrix)
    scores = nx.pagerank(nx_graph)
    
    # 5) Ordina le frasi per punteggio
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    
    # 6) Prendi le top_n
    summary = " ".join([s for _, s in ranked_sentences[:top_n]])
    return summary

# Esempio d’uso
text = """
I leader dei principali paesi europei hanno detto che un'eventuale pace in Ucraina non può essere discussa senza il presidente Volodymyr Zelensky, che non è stato incluso nel previsto incontro del 15 agosto tra il presidente degli Stati Uniti Donald Trump e quello russo Vladimir Putin.

Regno Unito, Francia, Germania, Italia, Polonia e Finlandia sostengono l'Ucraina nel tentativo di evitare che Stati Uniti e Russia si accordino per un cessate il fuoco che preveda condizioni che Zelensky ha sempre detto sarebbero inaccettabili, come la cessione di alcuni territori occupati dalla Russia dopo l'invasione cominciata nel 2022. Domenica Zelensky ha ringraziato i leader europei per aver sostenuto la sua richiesta di essere incluso nelle trattative, ribadita anche dal cancelliere tedesco Friedrich Merz, che ha detto di sperarla e di aspettarsela.
"""
print(textrank_summarize(text, top_n=2))
