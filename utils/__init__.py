"""
Utils Module
Contains utility functions and helpers for tests.
"""

from utils.test_helpers import (
    wait_for_network_idle,
    wait_for_dom_content_loaded,
    retry_with_backoff,
    get_random_string,
    get_current_timestamp,
    log_step,
    generate_test_summary,
    wait_and_click,
    wait_and_fill,
    get_random_email,
    take_screenshot_on_failure,
)

from utils.csv_loader import CSVDataLoader

__all__ = [
    "wait_for_network_idle",
    "wait_for_dom_content_loaded",
    "retry_with_backoff",
    "get_random_string",
    "get_current_timestamp",
    "log_step",
    "generate_test_summary",
    "wait_and_click",
    "wait_and_fill",
    "get_random_email",
    "take_screenshot_on_failure",
    "CSVDataLoader",
]
