import re

def epitopeMap(sequence, epitopes):
  matches = []
  # return [(m.start(0), m.end(0)) for m in re.finditer(epitope, sequence)]
  for epitope in epitopes:
    for value in [{'linearsequence': epitope,'init_pos': m.start(0)} for m in re.finditer(epitope, sequence)]:
      matches.append(value)

  return {'epitope_maps': matches}