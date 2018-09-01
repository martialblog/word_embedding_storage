# Storage and retrieval of Word Embeddings in various databases

Word Embeddings map lexical items to vectors of real numbers. These vectors can vary in size, in what is usually called dimensions. Besides creating your own embeddings, you can also use a variety of pretrained models.

The problem, however, when incorporating these models into an application is, that they usually have a large memory footprint. Google's pretrained Word2Vec embeddings (300 dimensions) have 3,4GB, Facebook's FastText embeddings  (300 dimensions) have 9,6GB. Loading the full model into memory can be a pain. For a more efficient retrieval, these tutorials will experiment with storing word embeddings in various databases.

## Databases

 - SQLite
 - MySQL
 - MongoDB
 - LevelDB

# Links and resouces

 - https://radimrehurek.com/gensim/
 - https://code.google.com/archive/p/word2vec/
 - https://github.com/facebookresearch/fastText
