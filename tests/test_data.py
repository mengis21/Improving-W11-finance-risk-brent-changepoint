from pathlib import Path

import numpy as np
import pandas as pd

from src.data import DatasetPaths, compute_log_returns, load_brent_prices, load_events


def test_dataset_paths_properties() -> None:
    paths = DatasetPaths(root=Path('/tmp/project'))
    assert paths.raw_prices_csv == Path('/tmp/project/data/raw/brent_oil_prices.csv')
    assert paths.raw_events_csv == Path('/tmp/project/data/raw/oil_market_events.csv')


def test_load_brent_prices_parses_and_sorts(tmp_path: Path) -> None:
    csv = tmp_path / 'prices.csv'
    csv.write_text(
        'Date,Price\n'
        '21-May-87,17.2\n'
        '20-May-87,17.1\n'
        'bad-date,20.0\n',
        encoding='utf-8',
    )

    df = load_brent_prices(csv)

    assert list(df.columns) == ['Date', 'Price']
    assert len(df) == 2
    assert df['Date'].is_monotonic_increasing
    assert df['Price'].dtype.kind in {'f', 'i'}


def test_load_events_parses_and_sorts(tmp_path: Path) -> None:
    csv = tmp_path / 'events.csv'
    csv.write_text(
        'event_date,event_title,event_type,region,notes\n'
        '2019-01-02,B event,Policy,Global,notes\n'
        'bad-date,drop me,Policy,Global,notes\n'
        '2018-12-30,A event,Sanctions,US/Iran,notes\n',
        encoding='utf-8',
    )

    df = load_events(csv)

    assert len(df) == 2
    assert df['event_date'].is_monotonic_increasing
    assert list(df['event_title']) == ['A event', 'B event']


def test_compute_log_returns_values() -> None:
    prices = pd.Series([100.0, 110.0, 121.0])
    returns = compute_log_returns(prices)

    expected = np.array([np.log(110.0 / 100.0), np.log(121.0 / 110.0)])
    assert np.allclose(returns.to_numpy(), expected)


def test_compute_log_returns_drops_first_nan() -> None:
    prices = pd.Series([10.0, 20.0])
    returns = compute_log_returns(prices)
    assert len(returns) == 1
