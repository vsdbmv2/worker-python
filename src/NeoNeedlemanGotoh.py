import numpy as np

negative_infinity = np.iinfo(np.int8).min
# np.iinfo(np.int64).min = Number.NEGATIVE_INFINITY
def process(s1, s2, pointers, lengths, M, Ms, G, Ge):
  pointers[0] = 0
  m = len(s1) + 1
  n = len(s2) + 1

  # Initializes the boundaries of the traceback matrix.
  # mat[x][y][1] =  0 - STOP
  # mat[x][y][1] = 1 - DIAGONAL
  # mat[x][y][1] = 2 - UP
  # mat[x][y][1] = 3 - LEFT
  k = n
  for i in range(1, m):
    pointers[k] = 3
    lengths[k] = i
    k += n
  for i in range(1, n):
    pointers[i] = 1
    lengths[i] = i
  v = np.zeros(n, dtype=np.int8)
  vDiagonal = 0# Float.NEGATIVE_INFINITY # best score in cell
  f = negative_infinity # score from diagonal
  h = negative_infinity # best score ending with gap from
  # left
  g = np.full(n, negative_infinity, dtype=np.int8) # best score ending with gap from above
  
  lengthOfHorizontalGap = 0
  lengthOfVerticalGap = np.empty(n, dtype=np.int8)

  similarityScore = None
  maximumScore = negative_infinity
  maxi = 0
  maxj = 0
  k = 0
  l = 0
  # Fill the matrices
  for i in range(1,m): # for all rows
    v[0] = -G - (i - 1) * Ge
    k = i * n
    for j in range(1, n): # for all columns
      l = k + j
      similarityScore = M if s1[i - 1] == s2[j - 1] else Ms
      f = vDiagonal + similarityScore # from diagonal
      # Which cell from the left?
      if (h - Ge) >= (v[j - 1] - G):
        h -= Ge
        lengthOfHorizontalGap+=1
      else:
        h = v[j - 1] - G
        lengthOfHorizontalGap = 1

      # Which cell from above?
      if (g[j] - Ge) >= (v[j] - G):
        g[j] = g[j] - Ge
        lengthOfVerticalGap[j] = lengthOfVerticalGap[j] + 1
      else:
        g[j] = v[j] - G
        lengthOfVerticalGap[j] = 1

      vDiagonal = v[j]

      v[j] = max(f, g[j], h) # best one
      if v[j] > maximumScore :
        maximumScore = v[j]
        maxi = i
        maxj = j

      # Determine the traceback direction
      # mat[x][y][1] =  0 - STOP
      # mat[x][y][1] = 1 - DIAGONAL
      # mat[x][y][1] = 2 - UP
      # mat[x][y][1] = 3 - LEFT
      if v[j] == f:
        pointers[l] = 2
      elif v[j] == g[j]:
        pointers[l] = 3
        lengths[l] = lengthOfVerticalGap[j]
      elif v[j] == h:
        pointers[l] = 1
        lengths[l] = lengthOfHorizontalGap
    # Reset
    h = negative_infinity
    vDiagonal = 0 # -o - (i - 1) * e
    lengthOfHorizontalGap = 0


  return { 'maxi': maxi, 'maxj': maxj, 'score': v[n - 1] }

def getFrom(als2):
  x = 0
  while (x < len(als2)):
    if (als2[x] == '-'):
      x += 1
    else:
      break
  return x

def getTo(als1, als2):
  x = len(als1) - 1
  while ((als2[x] == '-') and x > 0):
    x -= 1
  return x

def traceBack (s1, s2, rowa, cola, pointers, lengths):
  als1 = s1
  als2 = s2


  # maximum length after the aligned sequences
  maxlen = len(s1) + len(s2)

  reversed1 = np.zeros(maxlen, dtype=np.int8) # reversed sequence #1
  reversed2 = np.zeros(maxlen, dtype=np.int8) # reversed sequence #2

  len1 = 0 # length of sequence #1 after alignment
  len2 = 0 # length of sequence #2 after alignment

  c1, c2 = None, None

  i = rowa # traceback start row
  j = cola # traceback start col
  n = len(s2) + 1
  row = i * n

  a = len(s1) - 1
  b = len(s2) - 1

  if (a - i) > (b - j):
    while (a-i) > (b-j):
      reversed1[len1] = s1[a]
      reversed2[len2] = '-'
      len1 += 1
      len2 += 1
      a-=1
    while b > j:
      c1 = s1[a]
      c2 = s2[b]

      reversed1[len1] = c1
      reversed2[len2] = c2

      len1 -= 1
      len2 -= 1
      a -= 1
      b -= 1

  else:
    while (b - j) > (a - i):
      reversed1[len1] = '-'
      reversed2[len2] = als2[b]
      len1 += 1
      len2 += 1

    while a > (i -1):
      c1 = als1[a]
      c2 = als2[b]

      reversed1[len1] = c1
      reversed2[len2] = c2
      len1 += 1
      len2 += 1
      a -= 1
      b -= 1

  # Traceback flag, where true => continue and false => stop
  stillGoing = True
  while (stillGoing):
    l = row + j
    #console.log(row + ' - ' + pointers[l] + ' - ' + lengths[l])
    if (pointers[l]) == 3:
      for k in range(0,lengths[l]):
        i -= 1
        reversed1[len1] = als1[i]
        reversed2[len2] = '-'
        row -= n

        len1 += 1
        len2 += 1

      if (lengths[l] <= 0):
        row -= n

    elif (pointers[l]) == 2:
      i -= 1
      j -= 1
      c1 = als1[i]
      c2 = als2[j]
      reversed1[len1] = c1
      reversed2[len2] = c2
      len1 += 1
      len2 += 1
      row -= n
    elif (pointers[l]) == 1:
      for k in range(0, lengths[l]):
        j -= 1
        reversed1[len1] = '-'
        reversed2[len2] = als2[j]
        len1 += 1
        len2 += 1
    elif (pointers[l]) == 0:
      stillGoing = False

  als1 = reverse_text(reversed1)
  als2 = reverse_text(reversed2)
  to = getTo(als1, als2)
  From = getFrom(als2)

  return {
    'als1': als1,
    'als2': als2,
    'to': to,
    'from': From
  }

def reverse_text (text):
  return text[::-1]

def generateArray(size, fill):
  if fill:
    return [fill] * size
  return [None] * size

def computeGlobalAlignment(sequence_reference, sequence_to_align, idsequence):
  sequence_reference = list(sequence_reference)
  sequence_to_align = list(sequence_to_align)

  M = 2 #match
  Ms = -3 #missmatch
  G = 5 # gap
  Ge = 2 # ?
  # subMatrix = new SubstitutionMatrix(2, -3, 5, 2)
  # troca = false
  #swap
  if len(sequence_reference) < len(sequence_to_align):
    sequence_to_align, sequence_reference = sequence_reference, sequence_to_align

  seq_ref_length = len(sequence_reference) + 1
  seq_align_length = len(sequence_to_align) + 1
  size_array = seq_ref_length * seq_align_length
  pointers = np.zeros(size_array, dtype=np.int8) #bytes array
  lengths = np.zeros(size_array, dtype=np.int8) # int array


  processing_result = process(sequence_reference, sequence_to_align, pointers, lengths, M, Ms, G, Ge)
  maxi = processing_result['maxi']
  maxj = processing_result['maxj']

  traceback_result = traceBack(sequence_reference , sequence_to_align , maxi, maxj, pointers, lengths)

  coverage = (((traceback_result['to'] - traceback_result['from']) * 100) / len(sequence_reference))
  return {
    'idsequence': idsequence,
    'map_init': traceback_result['from'],
    'map_end': traceback_result.to,
    'coverage_pct': coverage.toFixed(2)
  }