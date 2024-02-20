# Task-Oriented Dialogue with In-Context Learning

Code for the Paper [Task-Oriented Dialogue with In-Context learning](https://arxiv.org/abs/2402.12234). 

Results are stored in `line-counts.json` and the `test-results` dir. 
To render a table of results, `pip install prettytable`, and run:

```
make show-results
```

You can also see the test conversations in the `e2e_tests` dir. 

### Installation & Setup

You need a Rasa Pro license to run the code.
You can get the free Rasa Pro Developer Edition [here](https://rasa.com/docs/rasa-pro/developer-edition/).

Install poetry, and then run

```
make install
```

Set the env var `RASA_PRO_LICENSE=<your rasa pro license key>`
If you want to run version_1, you'll need to set the env var `OPENAI_API_KEY=<your openai api key>`. 
Alternatively, you can edit `version_1/config.yml` to use a different LLM. Follow the instructions [here](https://rasa.com/docs/rasa-pro/concepts/components/llm-configuration#other-llmsembeddings).

### Training and testing a version of the bot:
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

CALM implementation. Business logic implemented. Referred to as "ours" in the arxiv paper.

**version_2**

Intent-based version, constrained to the CALM code budget. Not used in the paper, as it's too weak of a baseline.

**version_3**

Intent-based version with larger code budget, referred to as 'baseline' in the arxiv paper.
Note that version 3 is a superset of the implementation of version_2
and many files are symbolic links to the version_2 implementation. 
