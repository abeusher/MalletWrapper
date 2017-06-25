
import subprocess
import os


class Mallet(object):
    
    def __init__(self):
        pass

    def set_mallet_dir(self, mallet_dir):
        self.mallet_dir = mallet_dir
        if not os.path.isdir(mallet_dir + "MalletWrapper"):
            os.mkdir(mallet_dir + "MalletWrapper")
        self.output_dir = mallet_dir + "MalletWrapper/"
        
    def execute(self, command):
        # suppress stdout and stderr by stdout=open(os.devnull, 'w')
        subprocess.Popen(command, cwd=self.mallet_dir)

    def build_command(self, operation, kwargs):
        command = ["bin/mallet", operation]
        for key, value in kwargs.items():
            command.extend(["--" + key.replace("_", "-"), str(value)])
        return command

    def import_dir(self, **kwargs):
        kwargs["keep-sequence"] = True
        kwargs["output"] = self.output_dir + "import.mallet"
        command = self.build_command(operation="import-dir", kwargs=kwargs)
        self.execute(command)


    def import_file(self, **kwargs):
        kwargs["data"] = 1
        kwargs["keep-sequence"] = True
        kwargs["output"] = self.output_dir + "import.mallet"
        command = self.build_command(operation="import-file", kwargs=kwargs)
        self.execute(command)

    def train_topics(self, **kwargs):
        kwargs["input"] = self.output_dir + "import.mallet"
        kwargs["output-topic-keys"] = self.output_dir + "topic_keys.csv"
        kwargs["output-doc-topics"] = self.output_dir + "doc_topics.csv"
        kwargs["topic-word-weights-file"] = self.output_dir + "topic_word_weights.txt"
        command = self.build_command(operation="train-topics", kwargs=kwargs)
        self.execute(command)

classifier = Mallet()
classifier.set_mallet_dir("/Users/mike/mallet-2.0.8/")
classifier.import_dir(input="/Users/mike/Python/SampleDocs", remove_stopwords=True)
classifier.train_topics()


"""
bin/mallet import-dir --help
A tool for creating instance lists of FeatureVectors or FeatureSequences from text documents.

--input DIR...
  The directory containing text files to be classified
  Default is (null)
--output FILE
  Write the instance list to this file; Using - indicates stdout.
  Default is text.vectors
--preserve-case [TRUE|FALSE]
  If true, do not force all strings to lowercase.
  Default is false
--replacement-files FILE [FILE ...]
  files containing string replacements, one per line:
    'A B [tab] C' replaces A B with C,
    'A B' replaces A B with A_B
  Default is (null)
--deletion-files FILE [FILE ...]
  files containing strings to delete after replacements but before tokenization (ie multiword stop terms)
  Default is (null)
--remove-stopwords [TRUE|FALSE]
  If true, remove a default list of common English "stop words" from the text.
  Default is false
--stoplist-file FILE
  Instead of the default list, read stop words from a file, one per line. Implies --remove-stopwords
  Default is null
--extra-stopwords FILE
  Read whitespace-separated words from this file, and add them to either
   the default English stoplist or the list specified by --stoplist-file.
  Default is null
--stop-pattern-file FILE
  Read regular expressions from a file, one per line. Tokens matching these regexps will be removed.
  Default is null
--skip-header [TRUE|FALSE]
  If true, in each document, remove text occurring before a blank line.  This is useful for removing email or UseNet headers
  Default is false
--skip-html [TRUE|FALSE]
  If true, remove text occurring inside <...>, as in HTML or SGML.
  Default is false
--keep-sequence-bigrams [TRUE|FALSE]
  If true, final data will be a FeatureSequenceWithBigrams rather than a FeatureSequence.
  Default is false
--encoding STRING
  Character encoding for input file
  Default is UTF-8
--token-regex REGEX
  Regular expression used for tokenization.
   Example: "[\p{L}\p{N}_]+|[\p{P}]+" (unicode letters, numbers and underscore OR all punctuation) 
  Default is \p{L}[\p{L}\p{P}]+\p{L}
"""

"""
bin/mallet import-file --help
A tool for creating instance lists of feature vectors from comma-separated-values
--input FILE
  The file containing data to be classified, one instance per line
  Default is null
--output FILE
  Write the instance list to this file; Using - indicates stdout.
  Default is text.vectors
--line-regex REGEX
  Regular expression containing regex-groups for label, name and data.
  Default is ^(\S*)[\s,]*(\S*)[\s,]*(.*)$
--keep-sequence-bigrams [TRUE|FALSE]
  If true, final data will be a FeatureSequenceWithBigrams rather than a FeatureSequence.
  Default is false
--remove-stopwords [TRUE|FALSE]
  If true, remove a default list of common English "stop words" from the text.
  Default is false
--replacement-files FILE [FILE ...]
  files containing string replacements, one per line:
    'A B [tab] C' replaces A B with C,
    'A B' replaces A B with A_B
  Default is (null)
--deletion-files FILE [FILE ...]
  files containing strings to delete after replacements but before tokenization (ie multiword stop terms)
  Default is (null)
--stoplist-file FILE
  Instead of the default list, read stop words from a file, one per line. Implies --remove-stopwords
  Default is null
--extra-stopwords FILE
  Read whitespace-separated words from this file, and add them to either 
   the default English stoplist or the list specified by --stoplist-file.
  Default is null
--stop-pattern-file FILE
  Read regular expressions from a file, one per line. Tokens matching these regexps will be removed.
  Default is null
--preserve-case [TRUE|FALSE]
  If true, do not force all strings to lowercase.
  Default is false
--encoding STRING
  Character encoding for input file
  Default is UTF-8
--token-regex REGEX
  Regular expression used for tokenization.
  Example: "[\p{L}\p{N}_]+|[\p{P}]+" (unicode letters, numbers and underscore OR all punctuation) 
  Default is \p{L}[\p{L}\p{P}]+\p{L}
"""


"""
bin/mallet train-topics --help
A tool for estimating, saving and printing diagnostics for topic models, such as LDA.
--input FILENAME
  The filename from which to read the list of training instances.  Use - for stdin.  The instances must be FeatureSequence or FeatureSequenceWithBigrams, not FeatureVector
  Default is null
--evaluator-filename FILENAME
  A held-out likelihood evaluator for new documents.  By default this is null, indicating that no file will be written.
  Default is null
--output-topic-keys FILENAME
  The filename in which to write the top words for each topic and any Dirichlet parameters.  By default this is null, indicating that no file will be written.
  Default is null
--num-top-words INTEGER
  The number of most probable words to print for each topic after model estimation.
  Default is 20
--topic-word-weights-file FILENAME
  The filename in which to write unnormalized weights for every topic and word type.  By default this is null, indicating that no file will be written.
  Default is null
--output-topic-docs FILENAME
  The filename in which to write the most prominent documents for each topic, at the end of the iterations.  By default this is null, indicating that no file will be written.
  Default is null
--num-top-docs INTEGER
  When writing topic documents with --output-topic-docs, report this number of top documents.
  Default is 100
--output-doc-topics FILENAME
  The filename in which to write the topic proportions per document, at the end of the iterations.  By default this is null, indicating that no file will be written.
  Default is null
--doc-topics-threshold DECIMAL
  When writing topic proportions per document with --output-doc-topics, do not print topics with proportions less than this threshold value.
  Default is 0.0
--doc-topics-max INTEGER
  When writing topic proportions per document with --output-doc-topics, do not print more than INTEGER number of topics.  A negative value indicates that all topics should be printed.
  Default is -1
--num-topics INTEGER
  The number of topics to fit.
  Default is 10
--num-threads INTEGER
  The number of threads for parallel training.
  Default is 1
--num-iterations INTEGER
  The number of iterations of Gibbs sampling.
  Default is 1000
--num-icm-iterations INTEGER
  The number of iterations of iterated conditional modes (topic maximization).
  Default is 0
--no-inference true|false
  Do not perform inference, just load a saved model and create a report. Equivalent to --num-iterations 0.
  Default is false
--random-seed INTEGER
  The random seed for the Gibbs sampler.  Default is 0, which will use the clock.
  Default is 0
--optimize-interval INTEGER
  The number of iterations between reestimating dirichlet hyperparameters.
  Default is 0
--optimize-burn-in INTEGER
  The number of iterations to run before first estimating dirichlet hyperparameters.
  Default is 200
--use-symmetric-alpha true|false
  Only optimize the concentration parameter of the prior over document-topic distributions. This may reduce the number of very small, poorly estimated topics, but may disperse common words over several topics.
  Default is false
--alpha DECIMAL
  SumAlpha parameter: sum over topics of smoothing over doc-topic distributions. alpha_k = [this value] / [num topics]
  Default is 5.0
--beta DECIMAL
  Beta parameter: smoothing parameter for each topic-word. beta_w = [this value]
  Default is 0.01
"""
