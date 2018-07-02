print('hello,pycharm. Nice to meet you.')

from pymining import itemmining
transactions = (('a', 'b', "c"), ('b'), ('a'), ('a', 'c', 'd'), ('b', 'c'), ('b', 'c'))
relim_input = itemmining.get_relim_input(transactions)
report = itemmining.relim(relim_input, min_support=2)
print('relim frequence:')
print(report)


# Test performance of multiple algorithms
#from pymining import perftesting
#perftesting.test_itemset_perf()


print('frequent sequence:')
from pymining import seqmining
seqs = ( 'caabc', 'abcb', 'cabc', 'abbca')
freq_seqs = seqmining.freq_seq_enum(seqs, 2)
print(freq_seqs)
print('sorted->')
print(sorted(freq_seqs))


print('association rules:')
from pymining import itemmining, assocrules, perftesting
transactions = perftesting.get_default_transactions()
relim_input = itemmining.get_relim_input(transactions)
item_sets = itemmining.relim(relim_input, min_support=2)
rules = assocrules.mine_assoc_rules(item_sets, min_support=2, min_confidence=0.5)
print('rules->')
print(rules)

perftesting.test_itemset_perf()
