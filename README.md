## Code for the fact-check rationalization paper @ ACL 2021.

### Paper:
**Structurizing Misinformation Stories via Rationalizing Fact-Checks**  
Shan Jiang, Christo Wilson  
In *Proceedings of the Annual Meeting of the Association for Computational Linguistics*, 2021  
Paper available at: https://shanjiang.me/publications/acl21_paper.pdf

### Contact:
Shan Jiang (sjiang@ccs.neu.edu)

### General instructions.

Install required dependencies:
```
pip install -r requirements.txt
```

Download and process data following `README.md` in `[DATA_NAME]` folder:
```
cd data/[DATA_NAME]
```

Train models or analyze rationales with `run.py`:
```
python rationalize/run.py --mode=[MODE] --data_name=[DATA_NAME] --config_name=[CONFIG_NAME]
```

`[MODE]`:
- `train`: train a model.
- `evaluate`: evaluate a model.
- `output`: output rationales.
- `binarize`: binarize rationales to 0/1 (soft rationalization only).
- `vectorize`: generate vectors/embeddings for rationales.
- `cluster`: cluster rationales and plot figures.

`[DATA_NAME]`:
- `movie_reviews`: the dataset of movie reviews.
- `personal_attacks`: the dataset of fact-checks.
- `fact-checks`: the dataset of fact-checks.
- `glove`: pretrained GloVe embeddings.

`[CONFIG_NAME]`:
- e.g., `soft_rationalizer` or any `.config` files in `[DATA_NAME]` folder.

### Instructions for replicating results in the paper.

#### Replicating results for Table 1.

Here is the instruction to replicate the `movie_reviews` column of Table 1. To replicate another column simply replace `movie_reviews` to `personal_attacks` in all the command lines.

First make sure that the dataset and embeddings are prepared: 
```
cd data/movie_reviews
./prepare_data.sh
cd ../glove
./prepare_data.sh
cd ../..
```

Then, run the following command, each line corresponds to an experiment from h0-h3 and s0-s1:
```
python rationalize/run.py --mode=train --data_name=movie_reviews --config_name=hard_rationalizer          # h0
python rationalize/run.py --mode=train --data_name=movie_reviews --config_name=hard_rationalizer_w_domain # h1
python rationalize/run.py --mode=train --data_name=movie_reviews --config_name=hard_rationalizer_wo_regu  # h2
python rationalize/run.py --mode=train --data_name=movie_reviews --config_name=hard_rationalizer_w_anti   # h3
python rationalize/run.py --mode=train --data_name=movie_reviews --config_name=soft_rationalizer          # s0
python rationalize/run.py --mode=train --data_name=movie_reviews --config_name=soft_rationalizer_w_domain # s1
```

To replicate the results for s2-s3, run:
```
python rationalize/run.py --mode=output --data_name=movie_reviews --config_name=soft_rationalizer_w_domain
python rationalize/run.py --mode=binarize --data_name=movie_reviews --config_name=soft_rationalizer_w_domain
```

#### Replicating results for Figures 3-5.

We have logged data to plot Figures 3-5.

To plot Figure 3, run:
```
python rationalize/run.py --mode=cluster --data_name=fact-checks --config_name=soft_rationalizer_w_domain
```
The results can be found in `data/fact-checks/soft_rationalizer_w_domain.cluster`.

To plot Figures 4 and 5, run:
```
cd data/fact-checks
python result_visualizer.py
```
The results can be found in `data/fact-checks/soft_rationalizer_w_domain.results`.

If you would like to train the model from scratch, run the following command in sequence.
```
cd data/fact-checks
python data_downloader.py     # Download fact-checks.
python data_extractor.py      # Extract text from HTML.
python data_cleaner.py        # Clean fact-checks.
python data_word2vec.py       # Build word2vec.
cd ../..
python rationalize/run.py --mode=train --data_name=fact-checks --config_name=soft_rationalizer_w_domain
python rationalize/run.py --mode=output --data_name=fact-checks --config_name=soft_rationalizer_w_domain
python rationalize/run.py --mode=vectorize --data_name=fact-checks --config_name=soft_rationalizer_w_domain
cd data/fact-checks
python rationale_filterer.py  # Filter vectors.
cd ../..
python rationalize/run.py --mode=cluster --data_name=fact-checks --config_name=soft_rationalizer_w_domain
cd data/fact-checks
python rationale_mapper.py    # Map rationales.
python result_visualizer.py   # Plot results.
```




