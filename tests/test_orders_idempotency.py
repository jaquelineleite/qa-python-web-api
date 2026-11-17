"""Idempotency contract tests against an isolated local HTTP test double.

The fake API is intentionally small. These tests verify the contract of the
fixture, NOT idempotency support in JSONPlaceholder or a production service.
"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Barrier, Lock, Thread
from concurrent.futures import ThreadPoolExecutor

import pytest
import requests


@pytest.fixture
def orders_api():
    saved = {}
    created = []
    state_lock = Lock()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            if self.path != "/orders":
                self.send_error(404)
                return

            key = self.headers.get("Idempotency-Key")
            if not key:
                self._reply(400, {"error": "missing idempotency key"})
                return

            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length))
            except (ValueError, json.JSONDecodeError):
                self._reply(400, {"error": "invalid JSON"})
                return

            # Protect the check-and-create operation across handler threads.
            with state_lock:
                if key in saved:
                    previous_payload, response = saved[key]
                    if payload != previous_payload:
                        status, body = 409, {"error": "key reused with different payload"}
                    else:
                        status, body = 200, response
                else:
                    response = {"id": len(created) + 1, "status": "created"}
                    created.append(response)
                    saved[key] = (payload, response)
                    status, body = 201, response

            self._reply(status, body)

        def _reply(self, status, body):
            data = json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", created
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def create_order(base_url, key, payload):
    return requests.post(
        f"{base_url}/orders",
        json=payload,
        headers={"Idempotency-Key": key},
        timeout=5,
    )


def test_same_key_and_payload_does_not_duplicate_order(orders_api):
    base_url, created = orders_api
    payload = {"product": "book", "quantity": 1}

    first = create_order(base_url, "order-001", payload)
    replay = create_order(base_url, "order-001", payload)

    assert first.status_code == 201
    assert replay.status_code == 200
    assert first.json() == replay.json()
    assert len(created) == 1


def test_same_key_with_different_payload_is_rejected(orders_api):
    base_url, created = orders_api

    first = create_order(base_url, "order-002", {"quantity": 1})
    conflict = create_order(base_url, "order-002", {"quantity": 2})

    assert first.status_code == 201
    assert conflict.status_code == 409
    assert len(created) == 1


def test_distinct_keys_create_distinct_orders(orders_api):
    base_url, created = orders_api
    payload = {"product": "book", "quantity": 1}

    first = create_order(base_url, "order-003", payload)
    second = create_order(base_url, "order-004", payload)

    assert first.status_code == second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
    assert len(created) == 2


def test_missing_key_is_rejected_without_creation(orders_api):
    base_url, created = orders_api
    response = requests.post(
        f"{base_url}/orders", json={"quantity": 1}, timeout=5
    )

    assert response.status_code == 400
    assert len(created) == 0


def test_concurrent_same_key_creates_only_one_order(orders_api):
    """Simultaneous client calls must not create duplicate orders."""
    base_url, created = orders_api
    workers = 8
    start = Barrier(workers)

    def submit(_):
        start.wait(timeout=10)
        return create_order(base_url, "order-concurrent-001", {"quantity": 1})

    with ThreadPoolExecutor(max_workers=workers) as pool:
        responses = list(pool.map(submit, range(workers)))

    assert sorted(response.status_code for response in responses) == [200] * (workers - 1) + [201]
    assert len({response.json()["id"] for response in responses}) == 1
    assert len(created) == 1


def test_concurrent_distinct_keys_create_distinct_orders(orders_api):
    """Independent idempotency keys represent independent operations."""
    base_url, created = orders_api
    workers = 8
    start = Barrier(workers)

    def submit(index):
        start.wait(timeout=10)
        return create_order(base_url, f"order-concurrent-{index}", {"quantity": 1})

    with ThreadPoolExecutor(max_workers=workers) as pool:
        responses = list(pool.map(submit, range(workers)))

    assert all(response.status_code == 201 for response in responses)
    assert len({response.json()["id"] for response in responses}) == workers
    assert len(created) == workers
