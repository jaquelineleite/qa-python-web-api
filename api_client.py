"""Small HTTP boundary for the existing JSONPlaceholder user checks."""
import requests


def get_user(base_url, user_id, timeout=10):
    """GET one user; let Requests timeout/connection exceptions reach the caller."""
    return requests.get(f"{base_url}/users/{user_id}", timeout=timeout)
