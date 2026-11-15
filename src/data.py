from typing import Literal
from datasets import load_dataset
import pandas as pd

DATASET_ID = "BeIR/scifact"
DATASET_ID_QRELS = "BeIR/scifact-qrels"

def load_data(config: Literal["corpus", "queries"] = "corpus") -> pd.DataFrame:
    
    if config not in ["corpus", "queries"]:
        raise ValueError("Config must be corpus or queries.")

    dataset = load_dataset(DATASET_ID, config)
    return dataset[config].to_pandas()


def load_qrels(split: Literal["train", "test"] = "test") -> pd.DataFrame:
    
    if split not in ["train", "test"]:
        raise ValueError("Split must be train or test.")

    dataset = load_dataset(DATASET_ID_QRELS, split=split)
    df = dataset.to_pandas()
    df["query-id"], df["corpus-id"] = df["query-id"].astype(str), df["corpus-id"].astype(str)

    return df


def load_queries_for_split(split: Literal["train", "test"] = "test") -> pd.DataFrame:
    """Return only the queries that belong to one split.

    The `queries` config mixes train and test together with no split column,
    so the qrels for that split are the only record of which queries are in it.
    """
    split_ids = load_qrels(split)["query-id"].unique()
    queries = load_data("queries")

    return queries[queries["_id"].isin(split_ids)].reset_index(drop=True)
