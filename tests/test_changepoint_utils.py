import numpy as np
import pandas as pd

from src.changepoint import ChangePointSummary, nearest_event, summary_to_dict


def test_summary_to_dict_serializes_dataclass_fields() -> None:
    summary = ChangePointSummary(
        tau_index_median=10,
        tau_index_hdi_94=(8, 12),
        tau_date_median='2018-11-15',
        tau_date_hdi_94=('2018-10-30', '2018-12-03'),
        mu_before_mean=-0.01,
        mu_after_mean=0.02,
        sigma_before_mean=0.6,
        sigma_after_mean=1.3,
        prob_mu_after_gt_before=0.7,
    )

    payload = summary_to_dict(summary)

    assert payload['tau_index_hdi_94'] == [8, 12]
    assert payload['tau_date_hdi_94'] == ['2018-10-30', '2018-12-03']
    assert payload['prob_mu_after_gt_before'] == 0.7


def test_nearest_event_returns_best_match_within_window() -> None:
    events = pd.DataFrame(
        {
            'event_date': ['2018-11-05', '2020-01-01'],
            'event_title': ['Sanctions', 'Other'],
            'event_type': ['Sanctions', 'Policy'],
            'region': ['US/Iran', 'Global'],
            'notes': ['n1', 'n2'],
        }
    )

    result = nearest_event(target_date='2018-11-15', events=events, max_days=45)

    assert result is not None
    assert result['event_title'] == 'Sanctions'
    assert result['abs_days'] == 10


def test_nearest_event_returns_none_when_outside_window() -> None:
    events = pd.DataFrame(
        {
            'event_date': ['2010-01-01'],
            'event_title': ['Old event'],
            'event_type': ['Policy'],
            'region': ['Global'],
            'notes': ['n'],
        }
    )

    result = nearest_event(target_date='2018-11-15', events=events, max_days=45)
    assert result is None


def test_nearest_event_returns_none_for_empty_df() -> None:
    events = pd.DataFrame(columns=['event_date', 'event_title', 'event_type', 'region', 'notes'])
    assert nearest_event(target_date='2018-11-15', events=events, max_days=45) is None


def test_nearest_event_picks_closest_by_absolute_days() -> None:
    events = pd.DataFrame(
        {
            'event_date': ['2018-11-14', '2018-11-20'],
            'event_title': ['Closest', 'Farther'],
            'event_type': ['Policy', 'Policy'],
            'region': ['Global', 'Global'],
            'notes': ['n1', 'n2'],
        }
    )

    result = nearest_event(target_date='2018-11-15', events=events, max_days=45)
    assert result is not None
    assert result['event_title'] == 'Closest'
    assert result['abs_days'] == 1
