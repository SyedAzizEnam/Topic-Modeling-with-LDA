import scipy.io

MAT_FILE = 'classic400.mat'
MAT_FILE_2 = 'new400.mat'


def readfile():
  f = scipy.io.loadmat(MAT_FILE)
  # f is a dictionary containing the following keys: ['classicwordlist', '__header__', 'truelabels', '__version__', '__globals__', 'classic400']
  # The relevant ones are ['classicwordlist', 'truelabels', 'classic400']
  return f['classic400'], f['truelabels'], f['classicwordlist']


def analyze(x):
  doc_lengths = []
  for document in x:
    doc_lengths.append(document.sum())
  print doc_lengths
  print "Max, Min, Sum and Length"
  print max(doc_lengths)
  print min(doc_lengths)
  print sum(doc_lengths)/len(doc_lengths)
  print sum(doc_lengths)
  print len(doc_lengths)
  min_index = 2
  max_index = 1000
  for doc in x:
    if doc.indices[0] < min_index:
      min_index = doc.indices[0]
    if doc.indices[-1] > max_index:
      max_index = doc.indices[-1]
  print "min_index, max_index", min_index, max_index

#x, y, words = readfile()
#analyze(x)


