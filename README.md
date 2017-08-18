# MalletWrapper
A Python wrapper for [MALLET](http://mallet.cs.umass.edu/about.php). Topic modeling only, for now.

## Mallet Installation Instructions (Mac)
1. [Download](http://mallet.cs.umass.edu/download.php) the Mallet directory of files
2. [Download](http://www.oracle.com/technetwork/java/javase/downloads/index.html) JDK (if you don't already have it)
3. [Install](https://brew.sh) Homebrew (if you haven't already)
4. Install Ant (if you haven't already) via ```brew install ant```
```
cd /dir/containing/mallet-2.x.x
ant
```

## MalletWrapper Tutorial

```python
from MalletWrapper import Mallet

model = Mallet('/Users/mikeronayne/mallet-2.0.8/')
model.import_dir(input='/Users/mikeronayne/mallet-2.0.8/sample-data/web/en')
model.train_topics()

print(model.topic_keys)
print(model.doc_topics)
print(model.word_weights)
```

```python
{0: {'dirichlet': 0.5, 'words': ['rings', 'are', 'were', 'norway', 'ring', 'dust', 'only', 'number', 'may', 'moons', 'narrow', 'uranian', 'particles', 'discovered', 'uranus', 'survived', 'some', 'saga', 'including', 'system']}, ... }

{0: {'name': 'file:/Users/mikeronayne/mallet-2.0.8/sample-data/web/en/elizabeth_needham.txt', 'topics': {7: 0.3105263157894737, 6: 0.3, 1: 0.19473684210526315, 8: 0.07894736842105263, 0: 0.03684210526315789, 9: 0.02631578947368421, 2: 0.02631578947368421, 3: 0.015789473684210527, 5: 0.005263157894736842, 4: 0.005263157894736842}}, ... }

{0: {'elizabeth': 0.01, 'needham': 0.01, 'died': 0.01, 'may': 3.01, 'also': 0.01, 'known': 0.01, 'mother': 0.01, 'was': 0.01, 'english': 0.01, 'procuress': 0.01, 'and': 0.01, 'brothel-keeper': 1.01, 'th-century': 0.01, 'london': 0.01, ... }, ... }
```

## MalletWraper Documentation

### Constructor

```python
Mallet(mallet_dir, memory=1)
```

Parameter | Type | Description | Default
--- | --- | --- | ---
mallet_dir | str | File path of Mallet-2.x.x directory, with trailing slash
memory | int, float | Maximum gigabytes of memory to allocate to Mallet | 1

### Importing Data

#### Via Directory

```python
import_dir(**kwargs)
```

Parameter | Type | Description | Default
--- | --- | --- | ---
input | str, list | The directories containing text files to be classified, one directory per class | null
preserve_case | bool | If true, do not force all strings to lowercase. | False
replacement_files | str, list | Files containing string replacements, one per line: 'A B [tab] C' replaces A B with C; 'A B' replaces A B with A_B | null
deletion_files | str, list | Files containing strings to delete after replacements but before tokenization (ie multiword stop terms) | null
remove_stopwords | bool | If true, remove a default list of common English "stop words" from the text. | False
stoplist_file | str | Instead of the default list, read stop words from a file, one per line. Implies ```remove_stopwords``` | null
extra_stopwords | str | Read whitespace-separated words from this file, and add them to either the default English stoplist or the list specified by ```stoplist_file```. | null
stop_pattern_file | str | Read regular expressions from a file, one per line. Tokens matching these regexps will be removed. | null
skip_header | bool | If true, in each document, remove text occurring before a blank line. This is useful for removing email or UseNet header | False
skip_html | bool | If true, remove text occurring inside <...>, as in HTML or SGML. | False
gram_sizes | int, str | Include among the features all n-grams of sizes specified. For example, to get all unigrams and bigrams, use ```gram_sizes='1,2'```. This option occurs after the removal of stop words, if removed. | 1
encoding | str | Character encoding for input file | UTF-8
token_regex | str | Regular expression used for tokenization. Example: ```[\p{L}\p{N}_]+\|[\p{P}]+``` (unicode letters, numbers and underscore OR all punctuation) | ```\p{L}[\p{L}\p{P}]+\p{L}```
print_output | bool | If true, print a representation of the processed data to standard output. This option is intended for debugging. | False

#### Via File

```python
import_file(**kwargs)
```

Parameter | Type | Description | Default
--- | --- | --- | ---
input | str | The file containing data to be classified, one instance per line | null
line_regex | str | Regular expression containing regex-groups for label, name and data. | ```^(\S*)[\s,]*(\S*)[\s,]*(.*)$```
name | int | The index of the group containing the instance name. Use 0 to indicate that the name field is not used. | 1
data |int | The index of the group containing the data. | 3
remove_stopwords | bool | If true, remove a default list of common English "stop words" from the text. | False
replacement_files | str, list | Files containing string replacements, one per line: 'A B [tab] C' replaces A B with C; 'A B' replaces A B with A_B | null
deletion_files | str, list | Files containing strings to delete after replacements but before tokenization (ie multiword stop terms) | null
stoplist_file | str | Instead of the default list, read stop words from a file, one per line. Implies ```remove_stopwords``` | null
extra_stopwords | str | Read whitespace-separated words from this file, and add them to either the default English stoplist or the list specified by ```stoplist_file```. | null
stop_pattern_file | str | Read regular expressions from a file, one per line. Tokens matching these regexps will be removed. | null
preserve_case | bool | If true, do not force all strings to lowercase. | False
encoding | str | Character encoding for input file | UTF-8
token_regex | str | Regular expression used for tokenization. Example: ```[\p{L}\p{N}_]+\|[\p{P}]+``` (unicode letters, numbers and underscore OR all punctuation) | ```\p{L}[\p{L}\p{P}]+\p{L}```
print_output | bool | If true, print a representation of the processed data to standard output. This option is intended for debugging. | False

### Train Topics

```python
train_topics(**kwargs)
```

Parameter | Type | Description | Default
--- | --- | --- | ---
input | str | The filename from which to read the list of training instances. Use - for stdin. The instances must be FeatureSequence or FeatureSequenceWithBigrams, not FeatureVector | null
input_model | str | The filename from which to read the binary topic model. The ```input``` option is ignored. By default this is null, indicating that no file will be read. | null
input_state | str | The filename from which to read the gzipped Gibbs sampling state created by ```output_state```. The original input file must be included, using ```input```. By default this is null, indicating that no file will be read. | null
output_model | str | The filename in which to write the binary topic model at the end of the iterations. By default this is null, indicating that no file will be written. | null
output_state | str | The filename in which to write the Gibbs sampling state after at the end of the iterations. By default this is null, indicating that no file will be written. | null
output_model_interval | int | The number of iterations between writing the model (and its Gibbs sampling state) to a binary file. You must also set the output_model to use this option, whose argument will be the prefix of the filenames. | 0
output_state_interval | int | The number of iterations between writing the sampling state to a text file. You must also set the ```output_state``` to use this option, whose argument will be the prefix of the filenames. | 0
inferencer_filename | str | A topic inferencer applies a previously trained topic model to new documents. By default this is null, indicating that no file will be written. | null
evaluator_filename | str | A held-out likelihood evaluator for new documents. By default this is null, indicating that no file will be written. | null
output_topic_keys | str | The filename in which to write the top words for each topic and any Dirichlet parameters. By default this is null, indicating that no file will be written. | null
num_top_words | int | The number of most probable words to print for each topic after model estimation. | 20
show_topics_interval | int | The number of iterations between printing a brief summary of the topics so far. | 50
topic_word_weights_file | str | The filename in which to write unnormalized weights for every topic and word type. By default this is null, indicating that no file will be written. | null
word_topic_counts_file | str | The filename in which to write a sparse representation of topic-word assignments. By default this is null, indicating that no file will be written. | null
diagnostics_file | str | The filename in which to write measures of topic quality, in XML format. By default this is null, indicating that no file will be written. | null
xml_topic_report | str | The filename in which to write the top words for each topic and any Dirichlet parameters in XML format. By default this is null, indicating that no file will be written. | null
xml_topic_phrase_report | str | The filename in which to write the top words and phrases for each topic and any Dirichlet parameters in XML format. By default this is null, indicating that no file will be written. | null
output_topic_docs | str | The filename in which to write the most prominent documents for each topic, at the end of the iterations. By default this is null, indicating that no file will be written. | null
num_top_docs | int | When writing topic documents with ```output_topic_docs```, report this number of top documents. | 100
output_doc_topics | str | The filename in which to write the topic proportions per document, at the end of the iterations. By default this is null, indicating that no file will be written. | null
doc_topics_threshold | float | When writing topic proportions per document with ```output_doc_topics```, do not print topics with proportions less than this threshold value. | 0.0
doc_topics_max | int | When writing topic proportions per document with ```output_doc_topics```, do not print more than INTEGER number of topics. A negative value indicates that all topics should be printed. | -1
num_topics | int | The number of topics to fit. | 10
num_threads | int | The number of threads for parallel training. | 1
num_iterations | int | The number of iterations of Gibbs sampling. | 1000
num_icm_iterations | int | The number of iterations of iterated conditional modes (topic maximization). | 0
no_inference | bool | Do not perform inference, just load a saved model and create a report. Equivalent to ```num_iterations``` 0. | False
random_seed | int | The random seed for the Gibbs sampler. Default is 0, which will use the clock. | 0
optimize_interval | int | The number of iterations between reestimating dirichlet hyperparameters. | 0
optimize_burn_in | int | The number of iterations to run before first estimating dirichlet hyperparameters. | 200
use_symmetric_alpha | bool | Only optimize the concentration parameter of the prior over document-topic distributions. This may reduce the number of very small, poorly estimated topics, but may disperse common words over several topics. | False
alpha | float | SumAlpha parameter: sum over topics of smoothing over doc-topic distributions. alpha_k = [this value] / [num topics] | 5.0
beta | float | Beta parameter: smoothing parameter for each topic-word. beta_w = [this value] | 0.01

## Future Improvements

 * Provide interface to move away from file reading (e.g. no extra stopwords file)
 * Better error handling, especially checking for bad inputs
 * Classification
