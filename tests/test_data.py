from data import load_data, load_qrels, load_queries_for_split
import pytest

COLUMN_NAMES = ["_id", "title", "text"]
COLUMN_NAMES_QRELS = ["query-id", "corpus-id", "score"]


@pytest.mark.parametrize(
    "table, num_rows",
    [
        ("corpus", 5183),
        ("queries", 1109)
    ]
)
def test_dataset_config_returns_correct_row_length(request, table, num_rows):
    df = request.getfixturevalue(table)
    assert len(df) == num_rows

@pytest.mark.parametrize(
    "table",
    [
        "corpus",
        "queries"
    ]
)
def test_columns_names_are_correct(request, table):
    df = request.getfixturevalue(table)

    assert df.columns.to_list() == COLUMN_NAMES

def test_incorrect_config_raises_value_error():
    with pytest.raises(ValueError):
        df = load_data("nadia")


@pytest.mark.parametrize(
    "table, num_rows",
    [
        ("qrels_train", 919),
        ("qrels_test", 339)
    ]
)
def test_qrels_returns_correct_row_count(request, table, num_rows):
    df = request.getfixturevalue(table)
    assert len(df) == num_rows

@pytest.mark.parametrize(
    "table",
    [
        "qrels_test",
        "qrels_train"
    ]
)
def test_qrels_columns_names_are_correct(request, table):
    df = request.getfixturevalue(table)
    assert df.columns.to_list() == COLUMN_NAMES_QRELS


def test_incorrect_split_raises_value_error():
    with pytest.raises(ValueError):
        df = load_qrels("nadia")



def test_queries_row_count_is_correct():
    df = load_queries_for_split("test")
    assert len(df) == 300

@pytest.mark.parametrize(
    "table, column",
    [
        ("corpus", "corpus-id"),
        ("queries", "query-id")
    ]
)
def test_test_qrels_in_configs(request, qrels_test, table, column):
    dataset = request.getfixturevalue(table)

    assert qrels_test[column].isin(dataset["_id"]).all()
