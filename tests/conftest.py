"""Shared fixtures: each table is loaded once per test run, not once per test.

scope="session" means pytest calls each fixture the first time a test asks
for it, then hands every later test the same object. Tests must not modify
these DataFrames, or the tests that run after them will see the change.
"""
import pytest

from data import load_data, load_qrels


@pytest.fixture(scope="session")
def corpus():
    return load_data("corpus")


@pytest.fixture(scope="session")
def queries():
    return load_data("queries")


@pytest.fixture(scope="session")
def qrels_train():
    return load_qrels("train")


@pytest.fixture(scope="session")
def qrels_test():
    return load_qrels("test")
