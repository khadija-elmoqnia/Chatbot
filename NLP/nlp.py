
import re
import spacy
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import yaml
import os


question_cache = {}
def load_yaml(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at path: {file_path}")
        return None

    with open(file_path, 'r', encoding='utf-8') as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            return yaml_data
        except yaml.YAMLError as exc:
            print(f"YAML parsing error: {exc}")
            return None

def text_processing(text):
    # Normalisation: Suppression des caractères spéciaux
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Normalisation: suppression des mots vides
    stop_words = set(stopwords.words('french'))
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in stop_words]
    # Tokenization
    tokens = word_tokenize(text)
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(token) for token in tokens]
    # Convertir tous les mots en minuscules
    words = [word.lower() for word in words]
    lemmatized_words = [lemma.lower() for lemma in lemmatized_words]
    # Vectorisation/word embedding
    # Word2Vec 
    word2vec_model = Word2Vec(sentences=[tokens], vector_size=100, window=5, min_count=1, workers=4)
    return {
        'text': text,
        'cleaned_text': ' '.join(words),
        'lemmatized_words': lemmatized_words,
        'word2vec_model': word2vec_model,
    }

def similar(X, Y):
    nlp = spacy.load("fr_core_news_md")
    # Process input question using spaCy
    doc_X = nlp(X)
    # Process predefined question using spaCy
    doc_Y = nlp(Y)
    # Calculate Jaccard similarity based on lemmatized words
    lemmatized_X = set(text_processing(X)['lemmatized_words'])
    lemmatized_Y = set(text_processing(Y)['lemmatized_words'])
    jaccard_similarity = len(set(lemmatized_X).intersection(lemmatized_Y)) / len(set(lemmatized_X).union(lemmatized_Y))
    # Calculate similarity using cleaned text
    cleaned_text_similarity = doc_X.similarity(doc_Y)
    # Calculate similarity using lemmatized words
    lemmatized_similarity = len(lemmatized_X.intersection(lemmatized_Y)) / len(lemmatized_X.union(lemmatized_Y))
    # Calculate similarity using Word2Vec model
    word2vec_similarity = doc_X.similarity(doc_Y)
    # Calculate similarity using cosine similarity
    vector_X = doc_X.vector.reshape(1, -1)
    vector_Y = doc_Y.vector.reshape(1, -1)
    cosine_similarity_score = cosine_similarity(vector_X, vector_Y)[0][0]
    # Combine the similarity scores (you can adjust the weights based on importance)
    combined_similarity = (
        0.3 * cleaned_text_similarity +
        0.2 * lemmatized_similarity +
        0.2 * jaccard_similarity +
        0.3 * word2vec_similarity +
        0.2 * cosine_similarity_score)
    # Return True if the combined similarity score is greater than a threshold (e.g., 0.5)
    return combined_similarity > 0.5


def find_most_similar_question_nlp_combined(input_question, predefined_questions):
    #Optimisation de temps de reponseet de recherche
    if input_question in question_cache:
        return question_cache[input_question]
    nlp = spacy.load("fr_core_news_md")
    input_doc = nlp(input_question)
    most_similar_question = None
    highest_similarity_score = -1
    for predefined_question in predefined_questions:
        predefined_doc = nlp(predefined_question)
        # Calculate Jaccard similarity based on lemmatized words
        input_lemmas = set(text_processing(input_question)['lemmatized_words'])
        predefined_lemmas = set(text_processing(predefined_question)['lemmatized_words'])
        jaccard_similarity = len(set(input_lemmas).intersection(predefined_lemmas)) / len(set(input_lemmas).union(predefined_lemmas))
        # Calculate similarity using cleaned text
        cleaned_text_similarity = input_doc.similarity(predefined_doc)
        # Calculate similarity using lemmatized words
        input_lemmas = set(text_processing(input_question)['lemmatized_words'])
        predefined_lemmas = set(text_processing(predefined_question)['lemmatized_words'])
        lemmatized_similarity = len(input_lemmas.intersection(predefined_lemmas)) / len(input_lemmas.union(predefined_lemmas))
        # Calculate similarity using Word2Vec model
        word2vec_similarity = input_doc.similarity(predefined_doc)
        # Calculate similarity using cosine similarity
        input_vector = input_doc.vector.reshape(1, -1)
        predefined_vector = predefined_doc.vector.reshape(1, -1)
        cosine_similarity_score = cosine_similarity(input_vector, predefined_vector)[0][0]
        # Combine the similarity scores
        combined_similarity = (
            0.3 * cleaned_text_similarity + 0.2 * lemmatized_similarity + 0.2 * jaccard_similarity + 0.3 * word2vec_similarity +
            0.2 * cosine_similarity_score)
        # Update the most similar question if a higher similarity score is found
        if combined_similarity > highest_similarity_score:
            most_similar_question = predefined_question
            highest_similarity_score = combined_similarity
    if highest_similarity_score > 0.7:
        question_cache[input_question] = most_similar_question
        return most_similar_question
    else:
        return None


# Exemple d'utilisation de la fonction similar
question1 = "Comment puis-je prendre un rendez-vous?"
question2 = "Comment planifier un rendez-vous avec vous?"
are_similar = similar(question1, question2)
print(are_similar)




