
from chatbot.reponse import getResponse
from tkinter import *
from Interface_graphique.interface import interface

import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

interface(getResponse)