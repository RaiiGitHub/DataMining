**Frequent Item Set Mining**
```python
from pymining import itemmining
transactions = (('a', 'b', 'c'), ('b'), ('a'), ('a', 'c', 'd'), ('b', 'c'), ('b', 'c'))
relim_input = itemmining.get_relim_input(transactions)
report = itemmining.relim(relim_input, min_support=2)
report
{frozenset(['c']): 4,
frozenset(['c', 'b']): 3,
frozenset(['a', 'c']): 2,
frozenset(['b']): 4,
frozenset(['a']): 3}

# Test performance of multiple algorithms
from pymining import perftesting
perftesting.test_itemset_perf()
Random transactions generated with seed None

Done round 0
Done round 1
...
```
**Association Rules Mining**
```python
from pymining import itemmining, assocrules, perftesting
transactions = perftesting.get_default_transactions()
relim_input = itemmining.get_relim_input(transactions)
item_sets = itemmining.relim(relim_input, min_support=2)
rules = assocrules.mine_assoc_rules(item_sets, min_support=2, min_confidence=0.5)
rules
[(frozenset(['e']), frozenset(['b', 'd']), 2, 0.6666666666666666),
(frozenset(['b', 'e']), frozenset(['d']), 2, 1.0),
(frozenset(['e', 'd']), frozenset(['b']), 2, 0.6666666666666666),
(frozenset(['a']), frozenset(['b', 'd']), 2, 0.5),
...
>>> # e -> b, d with support 2 and confidence 0.66
>>> # b, e -> d with support 2 and confidence 1
```

**Frequent sequence mining**
```python
from pymining import seqmining
seqs = ( 'caabc', 'abcb', 'cabc', 'abbca')
freq_seqs = seqmining.freq_seq_enum(seqs, 2)
sorted(freq_seqs)

```