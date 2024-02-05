# tod-in-context-learning

Code for the Paper [Task-Oriented Dialogue with In-Context learning](#). 

Results are stored in `line-counts.json` and the `test-results` dir. 
To render a table of results, run:

```
make show-results
```

To train and test a specific version (e.g. 1, 2, or 3), run:

```
make train-version version=1
```

and 

```
make test-version version=1
```

### Versions

**version_1**

CALM implementation. Business logic implemented. 

**version_2**

intent-based version, constrained to the CALM code budget

**version_3**

intent-based version with larger code budget. 
Note that version 3 is a superset of the implementation of version_2
and many files are symbolic links to the version_2 implementation. 
