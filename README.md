# Storage and retrieval of Word Embeddings in various databases

Word Embeddings map lexical items to vectors of real numbers, thus representing lexical items in a mathematical and comparable way. These vectors can vary in size, this is usually called the dimensions of embeddings. Besides creating your own embeddings, you can also use a variety of pretrained models. For instance, Google's Word2Vec model or Facebook's FastText model. Various tutorials can be found out these. This tutorial is focused on storage and retrieval of word embeddings in various databases.

This is, because incorporating these models into a productive applicate can be a problem sometimes, since loading large amounts of embeddings into memory can be a pain. Google's pretrained Word2Vec embeddings (300 dimensions) have 3,4GB in size, Facebook's FastText embeddings (300 dimensions) around 10GB. Since we usually only want a certain subset of embeddings, we need a more efficient way for retrieval. Instead of loading the entire set into memory that is. Thus, we will experiment with storing word embeddings in various databases.

## Databases

 - SQLite
 - MySQL
 - MongoDB
 - LevelDB
 - PostgreSQL

## Results

![Read Times](readtimes.png?raw=true "Read Times")

![Write Times](writetimes.png?raw=true "Write Times")

![DB Sizes](dbsizes.png?raw=true "DB Sizes")

## Setup

``` bash
# Optional venv
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip3 install -r requirements.txt

# Start Jupyter Notebook
jupyter notebook
```

# Contributing

Contributions are welcome. Feel free to open a Pull Request or an Issue.

# Links and resouces

 - https://radimrehurek.com/gensim/
 - https://code.google.com/archive/p/word2vec/
 - https://github.com/facebookresearch/fastText
