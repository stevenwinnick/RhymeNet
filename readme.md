### RhymeNet
An English language database containing information about both words' phoenetic and written syllable divisions.

# Things you should definitely know
As far as I can tell, there is no agreed-upon best way to syllabize words (break them into syllables). This is understandable for many reasons, including the important one that each word can be pronounced in many ways. When creating this dataset, I chose to default to the way I personally hear syllables, specifically how I understand them in the context of song lyrics, as that is a field I envision this dataset being applied to for analysis. This often means that the phonetic syllable divisions differ from how one might be inclined to interpret the corresponding written ones by containing more non-vowel sounds at the start of each syllable. For example, most dictionaries (including the one this dataset is based on) syllabize the word "edit" as ed-it, but here it is phonetically syllabized as EH1 - D AH0 T, the way I would expect to hear it rhythmically. A fun project could be to try and redo the written syllables to line up with the phonetic ones.

To create this dataset, I started with version 0.7b of the CMU Pronouncing Dictionary, which contains the pronunciations of over 134,000 words via 39 phonemes based on the ARPAbet symbol set. I parsed these using the Greedy Onset Clustering method described below, then added the written syllabification of each of these words from the Project Gutenberg EBook of Webster's Unabridged Dictionary from August 22, 2009.

# Phonetic Syllabization: Greedy Onset Clustering
To syllabize words based on their phonemes, I use greedy onset clustering (see Anderson's Essentials of Linguistics in references). Essentially, syllables are constructed in a way that maximizes the number of non-vowel sounds at the start of each syllable. However, not all consonants after a vowel sound get sent to the start of the next syllable - there are a limited number of "consonant clusters" (Pearce) that are allowed. Again, there is much disagreement on what consonant clusters exist in English. To determine which to include in the algorithm to create this dataset, I followed the paper "What Consonant Clusters Are Possible?" (Alego), which examines a variety of studies into this question and gives explanations as to why some researchers consider some combinations to be clusters while others don't. I started by accepting all clusters that were included in all studies, then selecting based on my own opinions which others would be suitable for this task, often by searching the CMU dictionary for all examples of them and deeciding based on whichever way seemed correct more often, with the choice typically seeming fairly clear.

# References
John Algeo (1978) What Consonant Clusters Are Possible?, Word, 29:3, 206-224, DOI: 10.1080/00437956.1978.11435661
Catherine Anderson (2007) Essentials of Linguistics https://ecampusontario.pressbooks.pub/essentialsoflinguistics/
Michael Pearce (2007) The Routledge Dictionary of English Language Studies
CMU Pronouncing Dictionary http://www.speech.cs.cmu.edu/cgi-bin/cmudict
Webster's Unabridged Dictionary https://www.gutenberg.org/ebooks/29765