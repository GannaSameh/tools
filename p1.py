import requests
from bs4 import BeautifulSoup


# Fetch the HTML content of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Atlantis"
response = requests.get(url)
html_content = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the main content of the article
main_content = soup.find('div', {'id': 'bodyContent'}).text

# Save the extracted data to a structured file (e.g., text file)
with open("raw_data.txt", "w", encoding="utf-8") as file:
    file.write(main_content)

print("Data extraction complete. Raw data saved to 'raw_data.txt'.")
import re

# Load the raw data from the file
with open("raw_data.txt", "r", encoding="utf-8") as file:
    raw_data = file.read()

# Remove citations (e.g., [1], [2], etc.)
cleaned_data = re.sub(r'\[\d+\]', '', raw_data)

# Remove extra whitespace and special characters
cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip()

# Extract dates using Regex (e.g., "circa 9000 BC", "5th century BC")
dates = re.findall(r'\b(?:circa\s)?\d{1,4}\s?(?:BC|AD|century)\b', cleaned_data)

# Extract names (e.g., "Plato", "Poseidon")
names = re.findall(r'\b[A-Z][a-z]+\b', cleaned_data)

# Extract locations (e.g., "Atlantic Ocean", "Greece")
locations = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', cleaned_data)

# Save the cleaned data to a new file
with open("cleaned_data.txt", "w", encoding="utf-8") as file:
    file.write(cleaned_data)

print("Data cleaning complete. Cleaned data saved to 'cleaned_data.txt'.")

from collections import Counter

# Tokenize the cleaned data into words
words = cleaned_data.split()

# Count the frequency of each word
word_counts = Counter(words)

# Define keywords to analyze
keywords = ["Atlantis", "Plato", "ocean", "island"]

# Calculate keyword frequencies
keyword_frequencies = {keyword: word_counts[keyword] for keyword in keywords}

# Find the most common locations
common_locations = Counter(locations).most_common(5)

# Print analysis results
print("Basic Statistics:")
print(f"Total Words: {len(words)}")
print(f"Keyword Frequencies: {keyword_frequencies}")
print(f"Most Common Locations: {common_locations}")

import matplotlib.pyplot as plt

# Plot keyword frequencies
plt.figure(figsize=(10, 6))
plt.bar(keyword_frequencies.keys(), keyword_frequencies.values(), color='cornflowerblue')
plt.title("Keyword Frequencies in Atlantis Article")
plt.xlabel("Keyword")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.tight_layout()
plt.show()


# Most Common Locations Pie Chart
# Extract labels and values from most common locations
labels, values = zip(*common_locations)

# Pie chart
plt.figure(figsize=(8, 8))
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
plt.title("Top 5 Most Commonly Mentioned Locations")
plt.tight_layout()
plt.show()

#Word Cloud from Cleaned Text
from wordcloud import WordCloud

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_data)

# Display
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of Cleaned Atlantis Article")
plt.tight_layout()
plt.show()


#Date Mention Timeline Histogram
# Extract years from dates for plotting
def parse_year(date_str):
    match = re.search(r'(\d{1,4})\s?(BC|AD|century)?', date_str)
    if match:
        year, era = match.groups()
        year = int(year)
        return -year if era == "BC" else year
    return None

numeric_dates = [parse_year(d) for d in dates if parse_year(d) is not None]

# Plot histogram of date mentions
plt.figure(figsize=(10, 5))
plt.hist(numeric_dates, bins=15, color='salmon', edgecolor='black')
plt.title("Histogram of Historical Dates Mentioned")
plt.xlabel("Year")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()


import networkx as nx
# Create a mini co-occurrence network between keywords and locations
G = nx.Graph()

for sentence in re.split(r'[.!?]', cleaned_data):
    sentence_keywords = re.findall(r'\b(?:Atlantis|Plato|Solon|Poseidon|Athenians|Egyptians)\b', sentence, re.IGNORECASE)
    sentence_locations = re.findall(r'\b(?:Greece|Egypt|Mediterranean|Atlantic|Santorini|Azores|Doggerland)\b', sentence, re.IGNORECASE)

    for kw in sentence_keywords:
        for loc in sentence_locations:
            G.add_edge(kw.capitalize(), loc.capitalize())

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.6)
nx.draw(G, pos, with_labels=True, node_color="lightgreen", edge_color="gray", node_size=1500, font_size=12)
plt.title("Keyword-Location Co-occurrence Network")
plt.show()

import pandas as pd
import seaborn as sns

# HTML Tag Distribution
from collections import Counter

# Re-scrape with BeautifulSoup to count tags
tags = [tag.name for tag in soup.find_all()]
tag_counts = Counter(tags)
tag_df = pd.DataFrame(tag_counts.items(), columns=["Tag", "Count"]).sort_values(by="Count", ascending=False)

# Updated barplot code to fix the FutureWarning
plt.figure(figsize=(10, 6))
sns.barplot(data=tag_df.head(15), x="Count", y="Tag", hue="Tag", palette="coolwarm", legend=False)
plt.title("Top 15 Most Used HTML Tags on the Page")
plt.xlabel("Count")
plt.ylabel("HTML Tag")
plt.tight_layout()
plt.show()




import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import pandas as pd
import seaborn as sns

# Set page title and layout
st.set_page_config(page_title="Atlantis Analysis", layout="wide")

# Title of the app
st.title("Atlantis Wikipedia Page Analysis")
st.write("This app analyzes data extracted from the Wikipedia page on Atlantis.")

# Fetch and parse the Wikipedia page
@st.cache_data
def fetch_and_parse():
    url = "https://en.wikipedia.org/wiki/Atlantis"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_content = soup.find('div', {'id': 'bodyContent'}).text
    return main_content

# Data Cleaning
@st.cache_data
def clean_data(raw_data):
    # Remove citations
    cleaned_data = re.sub(r'\[\d+\]', '', raw_data)
    # Remove extra whitespace
    cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip()
    return cleaned_data

# Extract dates, names, and locations
@st.cache_data
def extract_entities(cleaned_data):
    dates = re.findall(r'\b(?:circa\s)?\d{1,4}\s?(?:BC|AD|century)\b', cleaned_data)
    names = re.findall(r'\b[A-Z][a-z]+\b', cleaned_data)
    locations = re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', cleaned_data)
    return dates, names, locations

# Analyze data
@st.cache_data
def analyze_data(cleaned_data, dates, locations):
    # Tokenize and count words
    words = cleaned_data.split()
    word_counts = Counter(words)
    keywords = ["Atlantis", "Plato", "ocean", "island"]
    keyword_frequencies = {keyword: word_counts[keyword] for keyword in keywords}
    common_locations = Counter(locations).most_common(5)
    return words, word_counts, keyword_frequencies, common_locations

# Streamlit UI
raw_data = fetch_and_parse()
cleaned_data = clean_data(raw_data)
dates, names, locations = extract_entities(cleaned_data)
words, word_counts, keyword_frequencies, common_locations = analyze_data(cleaned_data, dates, locations)

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Overview", "Keyword Frequencies", "Locations", "Word Cloud", "Date Timeline", "HTML Tags"])

# Overview Section
if section == "Overview":
    st.header("Overview")
    st.write("This section provides an overview of the extracted data.")
    st.write(f"**Total Words:** {len(words)}")
    st.write("**Keyword Frequencies:**")
    st.json(keyword_frequencies)
    st.write("**Most Common Locations:**")
    st.json(common_locations)

# Keyword Frequencies Section
elif section == "Keyword Frequencies":
    st.header("Keyword Frequencies")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(keyword_frequencies.keys(), keyword_frequencies.values(), color='cornflowerblue')
    ax.set_title("Keyword Frequencies in Atlantis Article")
    ax.set_xlabel("Keyword")
    ax.set_ylabel("Frequency")
    ax.grid(axis='y')
    st.pyplot(fig)

# Locations Section
elif section == "Locations":
    st.header("Most Common Locations")
    labels, values = zip(*common_locations)
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Pastel1.colors)
    ax.set_title("Top 5 Most Commonly Mentioned Locations")
    st.pyplot(fig)

# Word Cloud Section
elif section == "Word Cloud":
    st.header("Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_data)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title("Word Cloud of Cleaned Atlantis Article")
    st.pyplot(fig)

# Date Timeline Section
elif section == "Date Timeline":
    st.header("Date Timeline")
    def parse_year(date_str):
        match = re.search(r'(\d{1,4})\s?(BC|AD|century)?', date_str)
        if match:
            year, era = match.groups()
            year = int(year)
            return -year if era == "BC" else year
        return None

    numeric_dates = [parse_year(d) for d in dates if parse_year(d) is not None]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(numeric_dates, bins=15, color='salmon', edgecolor='black')
    ax.set_title("Histogram of Historical Dates Mentioned")
    ax.set_xlabel("Year")
    ax.set_ylabel("Frequency")
    ax.grid(True)
    st.pyplot(fig)

# HTML Tags Section
elif section == "HTML Tags":
    st.header("HTML Tags Distribution")
    tags = [tag.name for tag in BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/Atlantis").text, 'html.parser').find_all()]
    tag_counts = Counter(tags)
    tag_df = pd.DataFrame(tag_counts.items(), columns=["Tag", "Count"]).sort_values(by="Count", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=tag_df.head(15), x="Count", y="Tag", hue="Tag", palette="coolwarm", legend=False)
    ax.set_title("Top 15 Most Used HTML Tags on the Page")
    ax.set_xlabel("Count")
    ax.set_ylabel("HTML Tag")
    st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ using Streamlit")


