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

clf = Mallet('/Users/mikeronayne/mallet-2.0.8/')
clf.import_dir(input='/Users/mikeronayne/mallet-2.0.8/sample-data/web/en')
clf.train_topics()

print(clf.topic_keys)
print(clf.doc_topics)
print(clf.word_weights)
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
mallet_dir : str : file path of Mallet-2.x.x directory, with trailing slash
memory : int, float : maximum gigabytes of memory to allocate to Mallet

### Importing Data

#### Via Directory

```python
import_dir(**kwargs)
```

##### Parameters

Parameter | Type | Description | Default
--- | --- | --- | ---
config | file path | Read command option values from a file | null
input | directory path(s) | The directories containing text files to be classified, one directory per class | null
preserve_case | bool | If true, do not force all strings to lowercase. | False
replacement_files | path(s) | Files containing string replacements, one per line: 'A B [tab] C' replaces A B with C; 'A B' replaces A B with A_B | null
deletion_files | path(s) | Files containing strings to delete after replacements but before tokenization (ie multiword stop terms) | null
remove_stopwords | bool | If true, remove a default list of common English "stop words" from the text. | False
stoplist_file | file path | Instead of the default list, read stop words from a file, one per line. Implies ```remove_stopwords``` | null
extra_stopwords | file path | Read whitespace-separated words from this file, and add them to either the default English stoplist or the list specified by ```stoplist_file```. | null
stop_pattern_file | file path | Read regular expressions from a file, one per line. Tokens matching these regexps will be removed. | null
skip_header | bool | If true, in each document, remove text occurring before a blank line.  This is useful for removing email or UseNet header | False
skip_html | bool | If true, remove text occurring inside <...>, as in HTML or SGML. | False
gram_sizes | comma separated ints | Include among the features all n-grams of sizes specified. For example, to get all unigrams and bigrams, use ```gram_sizes='1,2'```. This option occurs after the removal of stop words, if removed. | 1
string_pipe | Pipe constructor | Java code for the constructor of a Pipe to be run as soon as input becomes a CharSequence | null
token_pipe | Pipe constructor | Java code for the constructor of a Pipe to be run as soon as input becomes a TokenSequence | null
fv_pipe | Pipe constructor | Java code for the constructor of a Pipe to be run as soon as input becomes a FeatureVector | Null
encoding | str | Character encoding for input file | UTF-8
token_regex | str | Regular expression used for tokenization. Example: ```[\p{L}\p{N}_]+\|[\p{P}]+``` (unicode letters, numbers and underscore OR all punctuation) | ```\p{L}[\p{L}\p{P}]+\p{L}```
print_output | bool | If true, print a representation of the processed data to standard output. This option is intended for debugging. | False
