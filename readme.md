# Rasa NLU Examples 

<img src="square-logo.svg" width=200 height=200 align="right">

This repository contains Rasa compatible machine learning components. These components 
are open sourced in order to encourage experimentation and to quickly offer support to
more tools. By hosting these components here they do not need to go through the same 
vetting process as the components in Rasa and we hope that this makes it easier for 
people to contribute new ideas. 

The components in the repository are **not officially supported**. There will be units tests
as well as documentation but this project should be considered a community project,
not something that is part of core Rasa. If there's a component here that turns out to be 
useful to the larger Rasa community then we might port features from this repository to Rasa. 

# Contribute 

There are many ways you can contribute to this project. 

- You can suggest new features. 
- You can help review new features. 
- You can submit new components.
- You can let us know if the components in this library help you. 

# Documentation

You can find the documentation for this project [here](https://rasahq.github.io/rasa-nlu-examples/).

# Features

This project currently supports components for Rasa 1.10. 

The following components are implemented;

### Meta

- `rasa_nlu_examples.meta.Printer`: a printer that's useful for debugging

### Dense Featurizers

- `rasa_nlu_examples.featurizers.dense.GensimFeaturizer`: pretrained gensim embeddings [link](https://radimrehurek.com/gensim/)
- `rasa_nlu_examples.featurizers.dense.FastTextFeaturizer`: pretrained fasttext embeddings [link](https://fasttext.cc/)
- `rasa_nlu_examples.featurizers.dense.BytePairFeaturizer`: pretrained byte-pair embeddings [link](https://nlp.h-its.org/bpemb/)

# Usage

You can install the examples from this repo via pip;

```
pip install git+https://github.com/RasaHQ/rasa-nlu-examples
```

Once installed you can add tools to your `config.yml` file, here's an example;

```yaml
language: en
pipeline:
- name: WhitespaceTokenizer
- name: CountVectorsFeaturizer
  OOV_token: oov.txt
  token_pattern: (?u)\b\w+\b
- name: CountVectorsFeaturizer
  analyzer: char_wb
  min_ngram: 1
  max_ngram: 4
- name: rasa_nlu_examples.featurizers.dense.BytePairFeaturizer
  lang: en
  vs: 1000
  dim: 25
- name: DIETClassifier
  epochs: 200
```

And you can use this file to run benchmarks. From the root folder of the project typically
that means running something like;

```
rasa test nlu --config basic-bytepair-config.yml \
          --cross-validation --runs 1 --folds 2 \
          --out gridresults/basic-bytepair-config
```