# 🧠 Natural Language Processing: Principles & Practice

<h3 align="center"><a href="README.md">中文</a> | <a href="README_en.md">English</a></h3>

> Teaching machines to understand human language — an NLP journey from scratch

## What is this?

A beginner-friendly course for people who **want to learn NLP but don't know where to start**.

This isn't a "here's a formula, go derive it yourself" kind of course — every lesson includes **hand-written algorithm implementations**. From tokenization to search engines to deep learning, 19 lessons take you from "What is NLP?" to "I can build a chatbot."

Each lesson wraps up with exercises and reference answers you can compare against. By the end, you'll understand: why search engines find what you're looking for, why machines can tell positive reviews from negative ones, and why chatbots can understand what you're saying.

## How do I run it?

```bash
# Install dependencies
pip install jieba gensim scikit-learn numpy torch transformers elasticsearch

# Navigate to a chapter
cd s_nlp/02_中文分词

# Run the demo
python main.py

# Do the exercises
python exercises.py
```

## What will I learn?

### Phase 1: Foundations 🏗️
Learn to make machines "read" Chinese first. Tokenization, POS tagging, named entity recognition — the bedrock of NLP.

| # | What you'll build | What you'll pick up along the way |
|---|-------------------|-----------------------------------|
| 01 | NLP landscape overview | What NLP is, what it can do, career paths |
| 02 | Chinese word segmenter | Rule-based segmentation, HMM, CRF, jieba in practice |
| 03 | POS tagger | HMM/perceptron/CRF part-of-speech tagging |
| 04 | Named entity recognition | Person/location/organization name recognition |
| 05 | Dependency parsing | Sentence structure, dependency relations |
| 06 | Semantic role labeling | "Who did what to whom" |

### Phase 2: Core Technologies ⚡
Start doing "useful stuff". Similarity computation, search engines, keyword extraction — NLP's core arsenal.

| # | What you'll build | What you'll pick up along the way |
|---|-------------------|-----------------------------------|
| 07 | Text similarity calculator | Edit distance, cosine similarity, Jaccard |
| 08 | Semantic similarity | Synonym dictionaries, DSSM, Sentence-BERT |
| 09 | TF-IDF keyword extraction | Term frequency-inverse document frequency, document similarity |
| 10 | Conditional random fields | CRF principles, feature templates, sequence labeling |
| 11 | New word discovery | Mutual information, left/right entropy, automatic word discovery |
| 12 | Simple search engine | Inverted index, Elasticsearch |

### Phase 3: Deep Learning & Practice 🚀
Enter the "advanced" territory. Word embeddings, text classification, deep learning — from traditional methods to neural networks.

| # | What you'll build | What you'll pick up along the way |
|---|-------------------|-----------------------------------|
| 13 | Word2Vec embeddings | CBOW/Skip-gram, gensim in practice |
| 14 | Text classifier | Naive Bayes/SVM/FastText/BERT |
| 15 | Text clustering | K-means, LDA topic modeling |
| 16 | Keywords & summarization | TextRank, extractive/abstractive summarization |
| 17 | Language models | N-Gram, LSTM, perplexity evaluation |
| 18 | Deep learning fundamentals | Neural networks/CNN/RNN/LSTM, PyTorch |
| 19 | Capstone projects | Chatbot, search engine, recommendation system |

## What does the file structure look like?

```
s_nlp/
├── 01_NLP概述/
│   ├── nlp_overview.py      ← Teaching module (detailed comments + real-life analogies)
│   ├── main.py              ← Runnable demo code
│   └── exercises.py         ← Exercises + reference answers
├── 02_中文分词/
│   ├── chinese_segmentation.py
│   ├── main.py
│   └── exercises.py
├── ...
├── 19_项目实战/
│   ├── chatbot.py           ← Chatbot
│   ├── search_engine.py     ← Search engine
│   └── recommend.py         ← Recommendation system
└── README.md                ← You're reading this one
```

## Tech Stack

- **Language**: Python 3.8+
- **NLP Tools**: jieba, gensim, sklearn, sklearn-crfsuite
- **Deep Learning**: PyTorch
- **Pretrained Models**: transformers (Hugging Face)
- **Search Engine**: elasticsearch (Python client)
- **Data Processing**: numpy, collections

## A Few Tips

1. **Don't skip chapters** — Each chapter builds on the previous one; skip ahead and you'll be lost
2. **Don't just read** — After running main.py, change the parameters, swap the data, and see how the results change
3. **Do the exercises** — They're not decoration; try writing them yourself before checking the answers
4. **Understand the principles** — Don't just memorize API calls; understanding the math behind the algorithms lets you use them flexibly
5. **Build something** — After finishing, try applying NLP to real problems like sentiment analysis or text classification

## Course Highlights

- 🧮 **Hand-written algorithms** — Core algorithms implemented from scratch, not through libraries, so you understand what's under the hood
- 🎯 **Practice-oriented** — Every lesson has a runnable demo, not just theory on paper
- 📝 **Exercises** — 3-5 per lesson, with TODO scaffolding + reference answers + test functions
- 💬 **Real-life analogies** — Complex concepts explained with everyday examples, lowering the barrier to understanding

---

> "Natural Language Processing = teaching machines to understand human language. After finishing this course, you'll be the one teaching machines to speak."
