
from collections import Counter
from time import perf_counter

REQUEST_COUNT = Counter()
TOTAL_LATENCY = Counter()


def track(endpoint, elapsed):
    REQUEST_COUNT[endpoint] += 1
    TOTAL_LATENCY[endpoint] += elapsed


def metrics():
    return {
        endpoint: {
            "requests": count,
            "average_latency_ms": round((TOTAL_LATENCY[endpoint] / count) * 1000, 2)
        }
        for endpoint, count in REQUEST_COUNT.items()
    }


def timed_call(endpoint, function, *args, **kwargs):
    started = perf_counter()
    try:
        return function(*args, **kwargs)
    finally:
        track(endpoint, perf_counter() - started)
