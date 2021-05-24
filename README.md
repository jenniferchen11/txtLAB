# txtLAB
txtlAB is a natural language processing and data science research labratory at McGill University. The Python scripts in this repository were created to conduct text analysis in a comparison between LGBTQ+ fanfictions and New York Times bestsellers. In particular, we focused on the three following forms of comparison:
1. Topic Modelling
2. Character Centrism
3. Events/Actions

## Overview of Methodologies
### Topic Modelling Methodology
The first method of analysis involved using topic modeling to search for recurring themes that emerge distinctively in one dataset but not the other. Several software libraries were employed in this process. To begin, Python’s Natural Language Toolkit filtered out the stop words of little significance (e.g. “the,” “and,” “but,” “or”). Then, Spacy was used to lemmatize the corpus; this ensured that different forms of a word (e.g. “organize” and “organizing”) were grouped together under one common base form. We then used a dictionary of words to create a bag of words (BoW) corpus. Finally, MALLET was used to create multiple term-topic matrices with each column containing 20 words belonging to a given topic. The process was repeated three times to create four different matrices with 20, 40, 60, 80 topic columns. It was determined that 40 topics allowed for extensive coverage of various topics, without there being considerable overlap of topics.

Character Centrism Methodology
In this section we executed a frequency analysis of the rate of characters in fanfiction v. mainstream fiction. To begin, we used David Bamman’s  BookNLP library to obtain tokens tables that provide data about every word in every corpus. We then counted the total number of words by counting each line in the tokens file and subtracting the ones with ‘deprel’ value ‘punct’ (i.e. we removed marks of punctuation). We discovered that entries labeled ‘punct’ would always outnumber any other ‘deprel’ tags, so we simply listed out the quantity of each deprel tag from greatest to least and added them all up, excluding the first one (which would be punctuation). Then, to get the character centric words, we filtered on two factors. First, we collected all words with ner tag ‘PERSON’, which means that the entry is the name of a character. Additionally, we collected any entry that had ‘she’, ‘he’, or ‘they’ in the lemma column. This would ensure that we collected all third person pronouns without including various forms of ‘it that would refer to an object rather than a character. Then, we calculated the two ratios by dividing character-centric words by total words.

Narrative Events Methodology
The aim in finding “narrative events” is to use the BookNLP tokens tables to identify the types of actions that most commonly occur in the two datasets. In our definition, an event is an action undertaken by an agent, potentially on an object. To collect and analyze our narrative events, we began by parsing through our bookNLP files and identifying the anchor verbs of each sentence. Anchor verbs were words that had both -1 for headTokenID and a verb POS tag (ie: VB, VBD, VBG, VBN, VBP, or VBZ). From there, we backtracked to find the subject associated with our anchor verb, a noun with deprel ‘nsubj’. Then, we verified that the nsubj was a person by running it through a list of strings for a match, checking its ner tag for ‘PERSON’ and checking its supersense for ‘noun.person’. Then, we collected the objects by forward tracking from the anchor verb to find a word with deprel ‘dobj’. For both the subject and object, we verified that they were associated by checking that its headTokenID pointed to the ID of the anchor verb. We built our bigrams with (subject, verb) and our trigrams with (subject, verb, object). 
In order to begin our analysis, we replaced all subjects and person-based objects with the word ‘Person’. To focus on the more common narrative events, we only kept the 1000 most frequently-parsed narrative events and removed the rest. With the remaining events, we built contingency tables using NumPy, and then found the log-likelihood of a given event being in a fanfiction corpus compared to a NYT corpus. Log-likelihood ratios were used rather than regular ratios to account for the fact that there were different numbers of occurrences for different narrative events, and events with more occurrences are more important for analysis. To aggregate verbs and objects into more general categories, we also grouped bigrams and trigrams by their supersense tags. For example, (‘Person’, ‘say’) turned into (‘Person’, ‘B-verb.communication’), and (‘Person’, ‘roll’, ‘eye’) became (‘Person’, ‘B-verb.motion’, ‘B-noun.body’). Finally, once log-likelihood values and their corresponding p-values were found using NumPy and SciPy, we sorted the events by their log-likelihood ratio values. 

## Getting Started

Download the files.

```bash
git clone https://github.com/jenniferchen11/txtLAB.git <FOLDER NAME>
```
Certain libraries require Anaconda environment.
Download Anaconda here: https://www.anaconda.com/products/individual

Creating a conda environment:

```bash
conda create -n name_of_my_env python
```
Other libraries may need to be downloaded as well:

```bash
conda install pandas
```

## Using Python Scripts

```bash
topic_model_2.py
```
Outputs 2 term topic matrices (k=35,40) AND a topic probability matrix for each data set.

```bash
bootstrap.p
```
Creates 1000 bootstrap samples from the topic probability matrix.

```bash
events.py
```
Captures bigrams and trigrams of (subject, action) or (subject, action, object).


