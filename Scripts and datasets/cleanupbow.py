import re
import scipy.io
import scipy.sparse
import numpy


VOCAB = "vocab.txt"
NEW_VOCAB = "newvocab.txt"
NEW_BOW = "newbagofwords.txt"
BOW = "bagofwords.txt"
MAT_FILE_2 = 'new400.mat'


def storeMat(bow, classic_word_list):
  bow_csc = scipy.sparse.csc_matrix(bow)
  truelabels = numpy.array([[1]*100 + [2]*100 + [3]*100 + [4]*100 + [5]*75])
  word_list = numpy.array([numpy.array([word]) for word in classic_word_list])
  d = {
    'classic400':bow_csc,
    'truelabels':truelabels,
    'classicwordlist':word_list,  # This doesn't work now.
  }
  scipy.io.savemat(MAT_FILE_2, d)
  # f is a dictionary containing the following keys: ['classicwordlist', '__header__', 'truelabels', '__version__', '__globals__', 'classic400']
  # The relevant ones are ['classicwordlist', 'truelabels', 'classic400']


def identifyWordsToDelete():
  count = 0
  word_index = 0
  word_to_delete = []
  classic_word_list = []
  for word in file(VOCAB):
    word = word.strip()
    if not re.match("^[A-Za-z_-]*$", word):
      #print word
      count += 1
      word_to_delete.append(word_index)
    elif len(word) <=2:
      #print word
      count += 1
      word_to_delete.append(word_index)
    else:
      classic_word_list.append(word)
    word_index += 1
  print count, word_index
  assert len(classic_word_list) + len(word_to_delete) == word_index
  return word_to_delete, classic_word_list

def generateCSC():
  word_to_delete, classic_word_list = identifyWordsToDelete()
  bow = []
  original_len = len(classic_word_list) + len(word_to_delete)
  for line in file(BOW):
    new_line = map(float, line.split())
    assert len(new_line) == original_len
    for word_index in word_to_delete[::-1]:   # We have to remove in reverse order!
      del new_line[word_index]
    assert len(new_line) == len(classic_word_list)
    bow.append(new_line)
  print len(bow)
  storeMat(bow, classic_word_list)
  #file(NEW_VOCAB, 'w').write('\n'.join(classic_word_list))

generateCSC()




