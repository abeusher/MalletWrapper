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
