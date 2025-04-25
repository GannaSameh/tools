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
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the app
st.title("FOODmart Supermarket Analysis")

# Load the dataset
@st.cache_data
def load_data():
    file_path = "StoresData.xlsx"
    data = pd.read_excel(file_path, sheet_name="Stores-Data")
    return data

data = load_data()

# Display raw data
st.header("Raw Data")
if st.checkbox("Show Raw Data"):
    st.write(data)

# Basic Statistics
st.header("Basic Statistics")
st.write("Number of Stores:", len(data))
st.write("Average Sales Revenue ($M):", round(data["Sales $m"].mean(), 2))
st.write("Average Wage Bill ($M):", round(data["Wages $m"].mean(), 2))

# Distribution of Stores by Location
st.header("Distribution of Stores by Location")
location_counts = data["Location"].value_counts()
fig1, ax1 = plt.subplots()
sns.barplot(x=location_counts.index, y=location_counts.values, palette="Blues_d", ax=ax1)
plt.title("Store Locations")
plt.xlabel("Location")
plt.ylabel("Count")
st.pyplot(fig1)

# Distribution of Stores by State
st.header("Distribution of Stores by State")
state_counts = data["State"].value_counts()
fig2, ax2 = plt.subplots()
sns.barplot(x=state_counts.index, y=state_counts.values, palette="Greens_d", ax=ax2)
plt.title("Stores by State")
plt.xlabel("State")
plt.ylabel("Count")
st.pyplot(fig2)

# Sunday Trading
st.header("Sunday Trading")
sunday_counts = data["Sundays"].value_counts()
fig3, ax3 = plt.subplots()
sns.barplot(x=sunday_counts.index, y=sunday_counts.values, palette="Oranges_d", ax=ax3)
plt.title("Sunday Trading")
plt.xlabel("Open on Sundays")
plt.ylabel("Count")
st.pyplot(fig3)

# Manager Gender
st.header("Manager Gender")
gender_counts = data["Mng-Sex"].value_counts()
fig4, ax4 = plt.subplots()
sns.barplot(x=gender_counts.index, y=gender_counts.values, palette="Purples_d", ax=ax4)
plt.title("Manager Gender")
plt.xlabel("Gender")
plt.ylabel("Count")
st.pyplot(fig4)

# Home Delivery
st.header("Home Delivery")
home_del_counts = data["HomeDel"].value_counts()
fig5, ax5 = plt.subplots()
sns.barplot(x=home_del_counts.index, y=home_del_counts.values, palette="Reds_d", ax=ax5)
plt.title("Home Delivery")
plt.xlabel("Home Delivery")
plt.ylabel("Count")
st.pyplot(fig5)

# Correlation Heatmap
st.header("Correlation Heatmap")
numeric_data = data.select_dtypes(include=["float64", "int64"])
corr_matrix = numeric_data.corr()
fig6, ax6 = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax6)
plt.title("Correlation Heatmap")
st.pyplot(fig6)

# Scatter Plot: Sales vs Wages
st.header("Sales vs Wages")
fig7, ax7 = plt.subplots()
sns.scatterplot(data=data, x="Sales $m", y="Wages $m", hue="Location", palette="Set1", ax=ax7)
plt.title("Sales vs Wages")
plt.xlabel("Sales ($M)")
plt.ylabel("Wages ($M)")
st.pyplot(fig7)

# Box Plot: Gross Profit by Location
st.header("Gross Profit by Location")
fig8, ax8 = plt.subplots()
sns.boxplot(data=data, x="Location", y="GrossProfit", palette="Set2", ax=ax8)
plt.title("Gross Profit by Location")
plt.xlabel("Location")
plt.ylabel("Gross Profit ($M)")
st.pyplot(fig8)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using [Streamlit](https://streamlit.io/)")



