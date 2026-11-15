# needle-search

Building search from scratch on the SciFact benchmark.

## Data card: SciFact (BEIR version)

### Source

| | |
|---|---|
| Original dataset | SciFact, Wadden et al., "Fact or Fiction: Verifying Scientific Claims" (EMNLP 2020). [allenai/scifact](https://github.com/allenai/scifact) |
| Version used here | The BEIR benchmark's retrieval version, loaded from the Hugging Face Hub |
| Corpus and queries | [`BeIR/scifact`](https://huggingface.co/datasets/BeIR/scifact) (configs `corpus` and `queries`) |
| Relevance labels (qrels) | [`BeIR/scifact-qrels`](https://huggingface.co/datasets/BeIR/scifact-qrels) (splits `train` and `test`) |
| Task | Given a scientific claim (the query), retrieve the paper abstracts that support or refute it |

### License

The licenses disagree depending on where you look, so both are recorded here:

- **Hugging Face (BEIR copies):** both `BeIR/scifact` and `BeIR/scifact-qrels` are tagged `cc-by-sa-4.0`.
- **Original SciFact repo ([LICENSE.md](https://github.com/allenai/scifact/blob/master/LICENSE.md)):** the claims and evidence annotations are CC BY 4.0, and the corpus abstracts come from Semantic Scholar's S2ORC and are ODC-By 1.0.

BEIR's own README says it only repackages public datasets and that checking permission to use each one is the user's job. This project follows the original licenses (attribution required) and cites the SciFact paper.

Checked on 2026-11-15.

### Sizes

| Piece | Rows | Notes |
|---|---|---|
| Corpus | 5,183 documents | Paper abstracts (title + abstract text) |
| Queries | 1,109 total | 809 train + **300 test**. Both splits live in one `queries` table |
| Qrels, train | 919 rows | Covers the 809 train queries |
| Qrels, test | 339 rows | Covers the 300 test queries, about 1.1 relevant documents per query |

The `queries` config does not say which split a query belongs to. To get the 300 test queries, keep only the query IDs that appear in the `test` split of `BeIR/scifact-qrels`.

### Schema

**Corpus** (`BeIR/scifact`, config `corpus`)

| Column | Type | Meaning |
|---|---|---|
| `_id` | string | Document ID (an S2ORC paper ID) |
| `title` | string | Paper title |
| `text` | string | Abstract |

**Queries** (`BeIR/scifact`, config `queries`)

| Column | Type | Meaning |
|---|---|---|
| `_id` | string | Query ID |
| `title` | string | Empty for SciFact |
| `text` | string | The claim |

**Qrels** (`BeIR/scifact-qrels`)

| Column | Type | Meaning |
|---|---|---|
| `query-id` | int64 | Matches `queries._id` |
| `corpus-id` | int64 | Matches `corpus._id` |
| `score` | int64 | Relevance; `1` means relevant |

Watch out: IDs are **strings** in the corpus and queries but **integers** in the qrels. Convert one side before joining, or every lookup comes back empty.

### Example

A test query and its relevant document, linked by the qrels row `query-id=1, corpus-id=31715818, score=1`:

- **Query `1`:** "0-dimensional biomaterials show inductive properties."
- **Relevant document `31715818`:** *New opportunities: the use of nanotechnologies to manipulate and track stem cells.* The abstract reviews how nanomaterials such as magnetic nanoparticles, quantum dots and carbon nanotubes can label, track and guide stem cells, and notes concerns about their toxicity.

Training query `0`, "0-dimensional biomaterials lack inductive properties.", points to the same document. SciFact pairs claims with their negations like this, so the document is relevant whether it supports or refutes the claim.

### Citation

```bibtex
@inproceedings{wadden-etal-2020-fact,
  title     = {Fact or Fiction: Verifying Scientific Claims},
  author    = {Wadden, David and Lin, Shanchuan and Lo, Kyle and Wang, Lucy Lu and van Zuylen, Madeleine and Cohan, Arman and Hajishirzi, Hannaneh},
  booktitle = {Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  year      = {2020}
}

@inproceedings{thakur2021beir,
  title     = {{BEIR}: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models},
  author    = {Thakur, Nandan and Reimers, Nils and R{\"u}ckl{\'e}, Andreas and Srivastava, Abhishek and Gurevych, Iryna},
  booktitle = {Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)},
  year      = {2021}
}
```
