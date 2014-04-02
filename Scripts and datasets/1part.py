import parse
import random
import sys
from select import select
from time import gmtime, strftime
import math

#logs = file("logs/testnewlogs%s.txt" % strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'w')
#zi_vals = file("logs/zi_vals%s.txt" % strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'w')
#q_vals = file("logs/q_vals%s.txt" % strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'w')

#theta_vals = file("logs/theta_vals%s.txt" % strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'w')

K = 4
M = 400
V= 6205

alpha = [0.33]*K
beta = [0.5]*V
sum_beta = sum(beta)
sum_alpha = sum(alpha)

q = []      # KxV matrix
n = []      # MxK matrix
z = []      # M many rows, each containing z_i values. Each z_i value is between 0 and K-1.

qbar = []   # K dim matrix, containing count of words in topic k

total_words = 31516
  

def setupz(x):
  global z, qbar, q, n, total_words
  
  # Initialize
  qbar = [0]*K
  for doc in x:
    n.append([0]*K)
  for j in xrange(K):
    q.append([0]*V)

  for m, doc in enumerate(x):
    w_i_index = 0
    w_count = doc[0, doc.indices[w_i_index]]
    w_i = doc.indices[w_i_index]
    z_m = []
    for i in xrange(int(doc.sum())):
      z_i_val = 0 #random.randint(0,K-1)
      z_m.append(z_i_val)
      if w_count == 0:
        w_i_index += 1
        w_i = doc.indices[w_i_index]
        w_count = doc[0, w_i]
      w_count -= 1
      q[z_i_val][w_i] += 1
      n[m][z_i_val] += 1
      qbar[z_i_val] +=1
    z.append(z_m)
  # Assert that the totals are correct.
  assert total_words == computesum(q)
  assert total_words == computesum(n)
  assert total_words == sum(qbar)

def computesum(twodarray):
  s = 0
  for row in twodarray:
    s+=sum(row)
  return s 

def selectWithDistribution(p):
  r = random.random()  # Rational number between 0 and 1
  for i in xrange(len(p)):
    r = r - p[i]
    if r<=0:
      return i
  raise Exception("Uh Oh... selectWithDistribution with r value %f" %r)

#Update formula.
# p(z_i=j) = (q'[j][w_i]+beta[w_i])/(sum_t (q'[j][t] + beta[t])) * (n'[m][j]+alpha[j])

def gibbsEpoch(x):
  shuffled_indices = [i for i in xrange(M)]
  #random.shuffle(shuffled_indices)
  for m in shuffled_indices:
    assert total_words == computesum(q)
    assert total_words == computesum(n)
    assert total_words == sum(qbar)
    doc = x.getrow(m)
    w_i_index = 0
    w_count = doc[0, doc.indices[w_i_index]]
    w_i = doc.indices[w_i_index]
    for i in xrange(int(doc.sum())):
      p = [0.0]*K
      if w_count == 0:
        w_i_index += 1
        w_i = doc.indices[w_i_index]
        w_count = doc[0, w_i]
      w_count -= 1
      # Look at current assignent of z_i and "unassign" it in q and n counts.
      old_j= z[m][i]
      q[old_j][w_i] -= 1
      n[m][old_j] -= 1
      qbar[old_j] -=1
      sum_p = 0.0
      for j in xrange(K):
        p[j] = (q[j][w_i]+beta[w_i])/(qbar[j] +sum_beta) * (n[m][j]+alpha[j])
        sum_p += p[j]
        #print p[j]
      #print sum_p
      for j in xrange(K):          # Normalize probability.
        p[j] = p[j] / sum_p
      new_j = selectWithDistribution(p)
      z[m][i] = new_j
      q[new_j][w_i] += 1
      n[m][new_j] += 1
      qbar[new_j] +=1

def computeFinalZi(x):
  for m, doc in enumerate(x):
    w_i_index = 0
    w_count = doc[0, doc.indices[w_i_index]]
    w_i = doc.indices[w_i_index]
    for i in xrange(int(doc.sum())):
      p = [0.0]*K
      if w_count == 0:
        w_i_index += 1
        w_i = doc.indices[w_i_index]
        w_count = doc[0, w_i]
      w_count -= 1
      # Look at current assignent of z_i and "unassign" it in q and n counts.
      old_j= z[m][i]
      q[old_j][w_i] -= 1
      n[m][old_j] -= 1
      qbar[old_j] -=1
      sum_p = 0.0
      for j in xrange(K):
        p[j] = (q[j][w_i]+beta[w_i])/(qbar[j] +sum_beta) * (n[m][j]+alpha[j])
      new_j = p.index(max(p))
      z[m][i] = new_j
      q[new_j][w_i] += 1
      n[m][new_j] += 1
      qbar[new_j] +=1

def computeConfidence():
  confidence = []
  for n_doc in n:
    conf = float(max(n_doc))/sum(n_doc)
    #print max(n_doc), sum(n_doc), conf
    confidence.append(conf)
  confidence = sorted(confidence)
  print confidence[0], confidence[100], confidence[200], confidence[300], confidence[-1]
  return confidence[0], confidence[100], confidence[200], confidence[300], confidence[-1]

def computeFinalTopic():
  final_topic = []
  for n_doc in n:
    topic = n_doc.index(max(n_doc))
    final_topic.append(topic)
  return final_topic

def readlineWithTimeout():
  timeout = 2
  print "Do you want to continue(y or n):"
  rlist, _, _ = select([sys.stdin], [], [], timeout)
  if rlist:
      s = sys.stdin.readline()
      return s.strip()
  else:
      print "No input. Moving on..."
      return 'y'


def computeTheta():
  theta = []
  for n_doc in n:
    tot = sum(n_doc)
    theta_doc = [float(val)/tot for val in n_doc]
    theta.append(theta_doc)
  return theta
    

bullshit = """
def computeTheta():
  # Returns a KxV matrix of Theta vectors. Each row corresponds to theta vector for one topic.
  theta = []
  for j in xrange(K):
    theta_j = [0.0]*V
    sigma_q = sum(q[j])
    denom = float(sigma_q) + sum_beta
    for w_i in xrange(V):
      theta_j[w_i] = (q[j][w_i] + beta[w_i])/denom
    theta.append(theta_j)
    print sum(theta_j)
  return theta


def computeP(theta, x):
  # Returns MxK array. Each row corresponds to a particular document.
  p = []
  for doc in x:
    num_words = (doc.sum())
    log_factorial_part = math.log(math.factorial(num_words))
    for i in xrange(doc.getnnz()):         # THis 'i' is different from the notation in notes.
      w_i = doc.indices[i]
      log_factorial_part -= math.log(math.factorial(doc[0, w_i]))
    log_p_doc = [log_factorial_part]*K
    for j in xrange(K):
      for i in xrange(doc.getnnz()):
        w_i = doc.indices[i]
        try:
          log_p_doc[j] += math.log(theta[j][w_i])*doc[0, w_i]
        except OverflowError as e:
          print log_p_doc[j], theta[j][w_i], doc[0, w_i]
          raise e
    p.append([math.e**val for val in log_p_doc])
  return p
"""


def computeTopWords(words):
  # For each topic, prints the top 25 words in that topic.
  top_n = 100
  #for topic in xrange(K)
  #  f[topic]=open(str(topic)+"Topwords","w")
  files = [open("topwords_topic%d.txt" % (topic), "w") for topic in xrange(K)]
  for topic in xrange(K):
    word_counts = list(q[topic])
    cut_off = sorted(word_counts, reverse=True)[top_n]
    top_words = []
    for i in xrange(V):
      if q[topic][i] >= cut_off:
        top_words.append((str(words[i,0][0]), q[topic][i]))
    top_words = sorted(top_words, reverse=True, key=lambda x: x[1])
   # for word,cnt in top_words
   #   f[topic].write(top)
    files[topic].write("\n".join(map(lambda x: x[0], top_words)))


def main():
  epoch = 200
  x, y, words = parse.readfile()
  setupz(x)
  confidence = [computeConfidence()]
  #logs.write("Epoch count, 0, 100, 200, 300, -1\n")
  for trial in xrange(epoch):
    if trial %25 == 0:
      print "In trial %d" % trial
    gibbsEpoch(x)
    if trial %25 == 0:
      confidence.append(computeConfidence())
    # if trial %25 == 0:
    #   logs.write(str(trial) + ", " +str(confidence[-1]) + "\n")
    """ if trial %100 == 0:
      print "computing top words. don't exit"
      decision = readlineWithTimeout()
      if decision == 'n':
        break"""
  computeTopWords(words)
  #computeFinalZi(x)    # Don't use this. This may be wrong!
  theta = computeTheta()
  #print "Theta"
  #print theta
  #for row in theta:
  #  theta_vals.write(",".join(map(str, row)) + "\n")
  """
  for row in z:
    zi_vals.write(str(row) + "\n")
  """
  #for row in q:
  #  q_vals.write(str(row) + "\n")
  # Read using this: map(int, x[1:-1].split(', '))
  final_comparison = []             # f_c[i][j] gives topic 'i' categorized as topic 'j'. Order of 'i's need not be same as order of 'j's
  for i in xrange(K):
    final_comparison_row = [0]*K
    final_comparison.append(final_comparison_row)
  final_topics = computeFinalTopic()
  for m in xrange(M):
    correct = y[0, m] -1  # -1 because the values are between 1 and K instead of 0 to k-1
    predicted = final_topics[m]
    final_comparison[correct][predicted] += 1
  print final_comparison
  #logs.write("Final comparison\n")
  #for row in final_comparison:
    #logs.write(str(row) + "\n")

main()


