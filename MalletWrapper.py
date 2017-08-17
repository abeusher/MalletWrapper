
import subprocess
import os
import re
import csv

class MalletError(Exception):
    pass

class Mallet(object):
    
    def __init__(self, mallet_dir, memory=1):
        self.memory = memory
        self.mallet_dir = mallet_dir
        self.set_memory()
        self.set_output_dir()

    def set_memory(self):
        # read
        with open(self.mallet_dir + 'bin/mallet.bat', 'r') as file :
          filedata = file.read()

        # replace memory line
        filedata = re.sub('set MALLET_MEMORY=.*', 'set MALLET_MEMORY=' + str(self.memory), filedata)

        # write
        with open(self.mallet_dir + 'bin/mallet.bat', 'w') as file:
          file.write(filedata)

    def set_output_dir(self):
        if not os.path.isdir(self.mallet_dir + 'MalletWrapper'):
            os.mkdir(self.mallet_dir + 'MalletWrapper')
        self.output_dir = self.mallet_dir + 'MalletWrapper/'
        self.stdout = self.output_dir + 'stdout.txt'
        
    def execute(self, command):
        result = subprocess.call(command, cwd=self.mallet_dir, stderr=subprocess.STDOUT, stdout=open(self.stdout, 'w'))

    def execute_exit_check(self, command, args):
        start = None
        for arg in args:
            if 'output' in arg:
                if os.path.isfile(args[arg]):
                    start = os.path.getmtime(args[arg])
                break
        self.execute(command)
        stop = None
        if os.path.isfile(args[arg]):
            stop = os.path.getmtime(args[arg])
        if not stop or start == stop:
            raise MalletError('\n\n' + args[arg] + ' was not generated from the command:\n\n"' + ' '.join(command) + 
                              '"\n\nCheck ' + self.output_dir + 'stdout.txt for details.\n')


    def build_command(self, operation, kwargs):
        command = ['bin/mallet', operation]
        for key, value in kwargs.items():
            command.extend(['--' + key.replace('_', '-'), str(value)])
        return command

    def import_dir(self, **kwargs):
        kwargs['keep_sequence'] = True # Topic modeling currently only supports feature sequences: use --keep-sequence option when importing data.
        kwargs['output'] = self.output_dir + 'import.mallet'
        command = self.build_command(operation='import-dir', kwargs=kwargs)
        self.execute_exit_check(command, kwargs)


    def import_file(self, **kwargs):
        #kwargs['data'] = 1
        kwargs['keep_sequence'] = True # Topic modeling currently only supports feature sequences: use --keep-sequence option when importing data.
        kwargs['output'] = self.output_dir + 'import.mallet'
        command = self.build_command(operation='import-file', kwargs=kwargs)
        self.execute_exit_check(command, kwargs)

    def train_topics(self, **kwargs):
        kwargs['input'] = self.output_dir + 'import.mallet'
        kwargs['output-topic-keys'] = self.output_dir + 'topic_keys.txt'
        kwargs['output-doc-topics'] = self.output_dir + 'doc_topics.txt'
        kwargs['topic-word-weights-file'] = self.output_dir + 'topic_word_weights.txt'
        if not kwargs.get('doc-topics-threshold', False):
            kwargs['doc-topics-threshold'] = 0.00001
        command = self.build_command(operation='train-topics', kwargs=kwargs)
        self.execute_exit_check(command, kwargs)
        self.parse_topic_keys()
        self.parse_doc_topics()
        self.parse_word_weights()

    def parse_topic_keys(self):
        self.topic_keys = dict()
        with open(self.output_dir + 'topic_keys.txt', mode='r', encoding='utf8') as file:
            for line in file:
                data = re.split('\t| ', line.strip())
                self.topic_keys[int(data[0])] = {'dirichlet': float(data[1]), 'words': self.process_words(data[2:])}
    
    def parse_doc_topics(self):
        self.doc_topics = dict()
        with open(self.output_dir + 'doc_topics.txt', mode='r', encoding='utf8') as file:
            next(file)
            for line in file:
                data = line.strip().split('\t')
                self.doc_topics[int(data[0])] = {'name': data[1], 'topics': self.process_topics(data[2:])}

    def parse_word_weights(self):
        self.word_weights = dict()
        with open(self.output_dir + 'topic_word_weights.txt', mode='r', encoding='utf8') as file:
            for line in file:
                data = line.strip().split('\t')
                try:
                    self.word_weights[int(data[0])][data[1]] = float(data[2])
                except KeyError:
                    self.word_weights[int(data[0])] = {data[1]: float(data[2])}

    @staticmethod
    def process_words(words):
        return [' '.join(x.split('_')) for x in words]

    @staticmethod
    def process_topics(topics):
        topic_weights = dict()
        for i in range(0, len(topics), 2):
            topic_weights[int(topics[i])] = float(topics[i+1])
        return topic_weights

    

#classifier = Mallet('/Users/mike/mallet-2.0.8/')
#classifier.import_dir(input='/Users/mike/mallet-2.0.8/sample-data/web/en')
#classifier.train_topics()



"""
bin/mallet import-dir --help
A tool for creating instance lists of FeatureVectors or FeatureSequences from text documents.

--help TRUE|FALSE
  Print this command line option usage information.  Give argument of TRUE for longer documentation
  Default is false
--prefix-code 'JAVA CODE'
  Java code you want run before any other interpreted code.  Note that the text is interpreted without modification, so unlike some other Java code options, you need to include any necessary 'new's when creating objects.
  Default is null
--config FILE
  Read command option values from a file
  Default is null
--input DIR...
  The directories containing text files to be classified, one directory per class
  Default is (null)
--output FILE
  Write the instance list to this file; Using - indicates stdout.
  Default is text.vectors
--use-pipe-from FILE
  Use the pipe and alphabets from a previously created vectors file. Allows the creation, for example, of a test set of vectors that are compatible with a previously created set of training vectors
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
--binary-features [TRUE|FALSE]
  If true, features will be binary.
  Default is false
--gram-sizes INTEGER,[INTEGER,...]
  Include among the features all n-grams of sizes specified.  For example, to get all unigrams and bigrams, use --gram-sizes 1,2.  This option occurs after the removal of stop words, if removed.
  Default is 1
--keep-sequence [TRUE|FALSE]
  If true, final data will be a FeatureSequence rather than a FeatureVector.
  Default is false
--keep-sequence-bigrams [TRUE|FALSE]
  If true, final data will be a FeatureSequenceWithBigrams rather than a FeatureVector.
  Default is false
--save-text-in-source [TRUE|FALSE]
  If true, save original text of document in source.
  Default is false
--string-pipe Pipe constructor
  Java code for the constructor of a Pipe to be run as soon as input becomes a CharSequence
  Default is null
--token-pipe Pipe constructor
  Java code for the constructor of a Pipe to be run as soon as input becomes a TokenSequence
  Default is null
--fv-pipe Pipe constructor
  Java code for the constructor of a Pipe to be run as soon as input becomes a FeatureVector
  Default is null
--encoding STRING
  Character encoding for input file
  Default is UTF-8
--token-regex REGEX
  Regular expression used for tokenization.
   Example: "[\p{L}\p{N}_]+|[\p{P}]+" (unicode letters, numbers and underscore OR all punctuation) 
  Default is \p{L}[\p{L}\p{P}]+\p{L}
--print-output [TRUE|FALSE]
  If true, print a representation of the processed data
   to standard output. This option is intended for debugging.
  Default is false
"""

"""
bin/mallet import-file --help
A tool for creating instance lists of feature vectors from comma-separated-values
--help TRUE|FALSE
  Print this command line option usage information.  Give argument of TRUE for longer documentation
  Default is false
--prefix-code 'JAVA CODE'
  Java code you want run before any other interpreted code.  Note that the text is interpreted without modification, so unlike some other Java code options, you need to include any necessary 'new's when creating objects.
  Default is null
--config FILE
  Read command option values from a file
  Default is null
--input FILE
  The file containing data to be classified, one instance per line
  Default is null
--output FILE
  Write the instance list to this file; Using - indicates stdout.
  Default is text.vectors
--line-regex REGEX
  Regular expression containing regex-groups for label, name and data.
  Default is ^(\S*)[\s,]*(\S*)[\s,]*(.*)$
--label INTEGER
  The index of the group containing the label string.
   Use 0 to indicate that the label field is not used.
  Default is 2
--name INTEGER
  The index of the group containing the instance name.
   Use 0 to indicate that the name field is not used.
  Default is 1
--data INTEGER
  The index of the group containing the data.
  Default is 3
--use-pipe-from FILE
  Use the pipe and alphabets from a previously created vectors file.
   Allows the creation, for example, of a test set of vectors that are
   compatible with a previously created set of training vectors
  Default is text.vectors
--keep-sequence [TRUE|FALSE]
  If true, final data will be a FeatureSequence rather than a FeatureVector.
  Default is false
--keep-sequence-bigrams [TRUE|FALSE]
  If true, final data will be a FeatureSequenceWithBigrams rather than a FeatureVector.
  Default is false
--label-as-features [TRUE|FALSE]
  If true, parse the 'label' field as space-delimited features.
     Use feature=[number] to specify values for non-binary features.
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
--print-output [TRUE|FALSE]
  If true, print a representation of the processed data
   to standard output. This option is intended for debugging.
  Default is false
"""


"""
bin/mallet train-topics --help
A tool for estimating, saving and printing diagnostics for topic models, such as LDA.
--help TRUE|FALSE
  Print this command line option usage information.  Give argument of TRUE for longer documentation
  Default is false
--prefix-code 'JAVA CODE'
  Java code you want run before any other interpreted code.  Note that the text is interpreted without modification, so unlike some other Java code options, you need to include any necessary 'new's when creating objects.
  Default is null
--config FILE
  Read command option values from a file
  Default is null
--input FILENAME
  The filename from which to read the list of training instances.  Use - for stdin.  The instances must be FeatureSequence or FeatureSequenceWithBigrams, not FeatureVector
  Default is null
--input-model FILENAME
  The filename from which to read the binary topic model. The --input option is ignored. By default this is null, indicating that no file will be read.
  Default is null
--input-state FILENAME
  The filename from which to read the gzipped Gibbs sampling state created by --output-state. The original input file must be included, using --input. By default this is null, indicating that no file will be read.
  Default is null
--output-model FILENAME
  The filename in which to write the binary topic model at the end of the iterations.  By default this is null, indicating that no file will be written.
  Default is null
--output-state FILENAME
  The filename in which to write the Gibbs sampling state after at the end of the iterations.  By default this is null, indicating that no file will be written.
  Default is null
--output-model-interval INTEGER
  The number of iterations between writing the model (and its Gibbs sampling state) to a binary file.  You must also set the --output-model to use this option, whose argument will be the prefix of the filenames.
  Default is 0
--output-state-interval INTEGER
  The number of iterations between writing the sampling state to a text file.  You must also set the --output-state to use this option, whose argument will be the prefix of the filenames.
  Default is 0
--inferencer-filename FILENAME
  A topic inferencer applies a previously trained topic model to new documents.  By default this is null, indicating that no file will be written.
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
--show-topics-interval INTEGER
  The number of iterations between printing a brief summary of the topics so far.
  Default is 50
--topic-word-weights-file FILENAME
  The filename in which to write unnormalized weights for every topic and word type.  By default this is null, indicating that no file will be written.
  Default is null
--word-topic-counts-file FILENAME
  The filename in which to write a sparse representation of topic-word assignments.  By default this is null, indicating that no file will be written.
  Default is null
--diagnostics-file FILENAME
  The filename in which to write measures of topic quality, in XML format.  By default this is null, indicating that no file will be written.
  Default is null
--xml-topic-report FILENAME
  The filename in which to write the top words for each topic and any Dirichlet parameters in XML format.  By default this is null, indicating that no file will be written.
  Default is null
--xml-topic-phrase-report FILENAME
  The filename in which to write the top words and phrases for each topic and any Dirichlet parameters in XML format.  By default this is null, indicating that no file will be written.
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
