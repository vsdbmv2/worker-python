from src.EpitopeMap import epitopeMap
from src.NeoNeedlemanGotoh import computeGlobalAlignment
from multiprocessing.pool import ThreadPool
# from src.Thread import Thread

def handleWorks (works):
  pool = ThreadPool(processes=len(works))
  threads = []
  results = []
  for work in works:
    if work['type'] == 'global-mapping':
      # Faz o mapeamento global
      thread = pool.apply_async(computeGlobalAlignment, (work['sequence1'], work['sequence2'], work['id1']))
      threads.append(thread)
    elif work['type'] == 'local-mapping':
      # faz a subtipagem
      pass
    elif work['type'] == 'epitope-mapping':
      # faz o mapeamento do epitopo
      # thread = Thread(target=epitopeMap, args=(work['sequence1'], work['epitopes']))
      # threads.append(thread)
      thread = pool.apply_async(epitopeMap, (work['sequence1'], work['epitopes']))
      threads.append(thread)
    else:
      print('Something wrong with the work, the payload type was incorrect or inexistent')
      print(work)
  # for thread in threads:
  #   thread.start()
  for thread in threads:
    # results.append(thread.join())
    results.append(thread.get())
  return results