import numpy as np
import pandas as pd
import pastastore as pst
import pytest

# %% write

# data
data = np.random.random_sample(int(1e5))
s = pd.Series(index=pd.date_range("1970", periods=1e5, freq="H"),
              data=data)
metadata = {"x": 100000., "y": 300000.}


def series_write(conn):
    conn.add_oseries(s, "oseries1", metadata=metadata, overwrite=True)


# @pytest.mark.benchmark(group="write_series")
# def test_benchmark_write_series_dict(benchmark):
#     conn = pst.DictConnector("test")
#     _ = benchmark(series_write, conn=conn)
#     return


@pytest.mark.benchmark(group="write_series")
def test_benchmark_write_series_pas(benchmark):
    conn = pst.PasConnector("test", "./tests/data/pas")
    _ = benchmark(series_write, conn=conn)
    return


@pytest.mark.benchmark(group="write_series")
def test_benchmark_write_series_pystore(benchmark):
    path = "./tests/data/pystore"
    conn = pst.PystoreConnector("test", path)
    _ = benchmark(series_write, conn=conn)
    return


@pytest.mark.benchmark(group="write_series")
def test_benchmark_write_series_arctic(benchmark):
    connstr = "mongodb://localhost:27017/"
    conn = pst.ArcticConnector("test", connstr)
    _ = benchmark(series_write, conn=conn)
    return

# %% read


def series_read(conn):
    _ = conn.get_oseries("oseries1")

# @pytest.mark.benchmark(group="read_series")
# def test_benchmark_write_series_dict(benchmark):
#     conn = pst.DictConnector("test")
#     _ = benchmark(series_read, conn=conn)
#     return


@pytest.mark.benchmark(group="read_series")
def test_benchmark_read_series_pas(benchmark):
    conn = pst.PasConnector("test", "./tests/data/pas")
    _ = benchmark(series_read, conn=conn)
    return


@pytest.mark.benchmark(group="read_series")
def test_benchmark_read_series_pystore(benchmark):
    path = "./tests/data/pystore"
    conn = pst.PystoreConnector("test", path)
    _ = benchmark(series_read, conn=conn)
    return


@pytest.mark.benchmark(group="read_series")
def test_benchmark_read_series_arctic(benchmark):
    connstr = "mongodb://localhost:27017/"
    conn = pst.ArcticConnector("test", connstr)
    _ = benchmark(series_read, conn=conn)
    return


# %% write model

def build_model(conn):

    store = pst.PastaStore("test", conn)

    # oseries nb1
    if "oseries_nb1" not in store.oseries.index:
        o = pd.read_csv("./tests/data/head_nb1.csv", index_col=0,
                        parse_dates=True)
        store.add_oseries(o, "oseries_nb1", metadata={"x": 100300,
                                                      "y": 400400})

    # prec nb1
    if "prec_nb1" not in store.stresses.index:
        s = pd.read_csv("./tests/data/rain_nb1.csv",
                        index_col=0, parse_dates=True)
        store.add_stress(s, "prec_nb1", kind="prec", metadata={"x": 100300,
                                                               "y": 400400})

    # evap nb1
    if "evap_nb1" not in store.stresses.index:
        s = pd.read_csv("./tests/data/evap_nb1.csv",
                        index_col=0, parse_dates=True)
        store.add_stress(s, "evap_nb1", kind="evap", metadata={"x": 100300,
                                                               "y": 400400})

    ml = store.create_model("oseries_nb1", add_recharge=True)

    return ml


def write_model(conn, ml):
    conn.add_model(ml, overwrite=True)


# @pytest.mark.benchmark(group="write_model")
# def test_benchmark_write_model_dict(benchmark):
#     conn = pst.DictConnector("test")
#     ml = build_model(conn)
#     _ = benchmark(write_model, conn=conn, ml=ml)
#     return


@pytest.mark.benchmark(group="write_model")
def test_benchmark_write_model_pas(benchmark):
    conn = pst.PasConnector("test", "./tests/data/pas")
    ml = build_model(conn)
    _ = benchmark(write_model, conn=conn, ml=ml)
    return


@pytest.mark.benchmark(group="write_model")
def test_benchmark_write_model_pystore(benchmark):
    path = "./tests/data/pystore"
    conn = pst.PystoreConnector("test", path)
    ml = build_model(conn)
    _ = benchmark(write_model, conn=conn, ml=ml)
    return


@pytest.mark.benchmark(group="write_model")
def test_benchmark_write_model_arctic(benchmark):
    connstr = "mongodb://localhost:27017/"
    conn = pst.ArcticConnector("test", connstr)
    ml = build_model(conn)
    _ = benchmark(write_model, conn=conn, ml=ml)
    return

# %%


def write_model_checkts(conn, ml):
    conn.check_model_series_values = True
    conn.add_model(ml, overwrite=True)


@pytest.mark.benchmark(group="write_model")
def test_benchmark_write_model_checkts_pas(benchmark):
    conn = pst.PasConnector("test", "./tests/data/pas")
    ml = build_model(conn)
    _ = benchmark(write_model_checkts, conn=conn, ml=ml)
    return


@pytest.mark.benchmark(group="write_model")
def test_benchmark_write_model_checkts_pystore(benchmark):
    path = "./tests/data/pystore"
    conn = pst.PystoreConnector("test", path)
    ml = build_model(conn)
    _ = benchmark(write_model_checkts, conn=conn, ml=ml)
    return


@pytest.mark.benchmark(group="write_model")
def test_benchmark_write_model_checkts_arctic(benchmark):
    connstr = "mongodb://localhost:27017/"
    conn = pst.ArcticConnector("test", connstr)
    ml = build_model(conn)
    _ = benchmark(write_model_checkts, conn=conn, ml=ml)
    return
# %% read model


def read_model(conn):
    ml = conn.get_models("oseries_nb1")
    return ml

# @pytest.mark.benchmark(group="read_model")
# def test_benchmark_read_model_dict(benchmark):
#     conn = pst.DictConnector("test")
#     _ = benchmark(read_model, conn=conn, ml=ml)
#     return


@pytest.mark.benchmark(group="read_model")
def test_benchmark_read_model_pas(benchmark):
    conn = pst.PasConnector("test", "./tests/data/pas")
    _ = benchmark(read_model, conn=conn)
    pst.util.delete_pas_connector(conn)
    return


@pytest.mark.benchmark(group="read_model")
def test_benchmark_read_model_pystore(benchmark):
    path = "./tests/data/pystore"
    conn = pst.PystoreConnector("test", path)
    _ = benchmark(read_model, conn=conn)
    pst.util.delete_pystore_connector(conn=conn)
    return


@pytest.mark.benchmark(group="read_model")
def test_benchmark_read_model_arctic(benchmark):
    connstr = "mongodb://localhost:27017/"
    conn = pst.ArcticConnector("test", connstr)
    _ = benchmark(read_model, conn=conn)
    pst.util.delete_arctic_connector(conn=conn)
    return