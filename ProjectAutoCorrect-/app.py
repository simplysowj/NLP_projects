import streamlit as st
import re
from collections import Counter

# Function to extract all the words from the text file
def words(text): 
    return re.findall(r'\w+', text.lower())

# Function to generate all the candidates that are 1 edit distance from the original word
def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    letters = 'abcdefghijklmnopqrstuvwxyz'
    deletion = [a + b[1:] for a, b in splits if b]
    insertion = [a + c + b for a, b in splits for c in letters]
    substitution = [a + c + b[1:] for a, b in splits if b for c in letters]
    transpose = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    return set(deletion + insertion + substitution + transpose)

# Function to keep only those candidates which are present in the vocabulary
def known(words, vocab):
    return set(w for w in words if w in vocab)

# Function to return the probability of a word
def P(word, vocab, N=None):
    if N is None:
        N = sum(vocab.values())
    return vocab[word] / N if word in vocab else 0


# Function to generate the candidates
def candidates(word, vocab): 
    return list(known([word], vocab)) or list(known(edits1(word), vocab)) or [word]

# Function to pick the best word out of the generated candidates
def correction(word, vocab): 
    return max(candidates(word, vocab), key=lambda w: P(w, vocab))

# Function to return the auto-corrected sentence
def sentence_corrector(sentence, vocab):
    tokens = sentence.lower().split()
    corrected_sentence = [correction(token, vocab) for token in tokens]
    return " ".join(corrected_sentence)

# Read the dataset
file_content = open('big.txt').read()
WORDS = Counter(words(file_content))

# Streamlit app
st.title("Spelling Corrector")

input_sentence = st.text_input("Enter a sentence:")
if input_sentence:
    corrected_sentence = sentence_corrector(input_sentence, WORDS)
    st.write("Corrected sentence:", corrected_sentence)
