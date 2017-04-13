# textrank
textrank is a Python package of `TextRank` proposed by following paper.

```
TextRank: Bringing Order into Texts, Mihalcea+, EMNLP 2004.
https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf
```
Note that, the keyword extraction method that also proposed by this paper is not supported.

TextRank is a graph-based summarization model based on PageRank like algorithm.
Any tokenization and normalization of texts does not performed on the scripts, so you should preprocess your data beforehand.  

# Example
```python
from text_rank import TextRank

tr = TextRank()

sentences = [
	"Hurricane Gilbert swept toward the Dominican Republic Sunday and the Civil Defense alerted its heavily populated south coast to prepare for high winds heavy rains and high seas",
        "The storm was approaching from the southeast with sustained winds of 75 mph gusting to 92 mph",
        "There is no need for alarm Civil Defense Director Eugenio Cabral said in a television alert shortly before midnight Saturday"]

sents_tokens = [sent.split(" ") for sent in sentences]

# set sentences that you want to summarize in the TextRank instance.
# the sentences need to be represented as a list of tokens.
tr.set_sentences(sents_toks)

# run TextRank algorithm and TextRank score for sentences
# if you set debug=True, #_of_iteration and convergence information will be presented.
tr.run(debug=True)

# you can access the final TextRank score as TextRank instance property
# tr.textrank[i] representes final TextRank score for i-th sentence
print tr.textrank
```
