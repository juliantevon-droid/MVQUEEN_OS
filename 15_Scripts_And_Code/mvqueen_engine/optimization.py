# ---------------------------------------------------------
# MVQUEEN OMNILUXE ENGINE — ANDROID OPTIMIZATION LAYER (BLOCK N)
# ---------------------------------------------------------

import hashlib
import json
import os
import threading

# ---------------------------------------------------------
# PORTABLE ANDROID-SAFE CACHE DIRECTORY
# ---------------------------------------------------------

BASE_DIR = os.path.expanduser("~/.mvqueen_cache")
os.makedirs(BASE_DIR, exist_ok=True)

_lock = threading.Lock()

# ---------------------------------------------------------
# CHUNKING UTILITIES
# ---------------------------------------------------------

def chunk_text(text: str, size: int = 200):
    """
    Splits text into safe Android-friendly chunks.
    Deterministic and stable.
    """
    return [text[i:i + size] for i in range(0, len(text), size)]

# ---------------------------------------------------------
# MEMORY-SAFE STREAMING
# ---------------------------------------------------------

def stream_process(text: str, processor_fn):
    """
    Streams text chunks through the processor to avoid RAM spikes.
    Returns a list of partial results.
    """
    chunks = chunk_text(text)
    results = []
    for c in chunks:
        results.append(processor_fn(c))
    return results

# ---------------------------------------------------------
# CACHE HELPERS
# ---------------------------------------------------------

def _cache_key(text: str) -> str:
    """
    Deterministic SHA-256 key for caching.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def cache_get(text: str):
    """
    Load cached result if available.
    """
    key = _cache_key(text)
    path = os.path.join(BASE_DIR, key + ".json")

    if not os.path.exists(path):
        return None

    with _lock:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

def cache_set(text: str, data: dict):
    """
    Save result to cache safely.
    """
    key = _cache_key(text)
    path = os.path.join(BASE_DIR, key + ".json")

    with _lock:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

# ---------------------------------------------------------
# LOW-RAM MODE
# ---------------------------------------------------------

def low_ram_process(text: str, processor_fn):
    """
    Uses caching + chunking to avoid memory spikes.
    If cached, returns cached result.
    Otherwise processes and caches.
    """
    cached = cache_get(text)
    if cached is not None:
        return cached

    result = processor_fn(text)
    cache_set(text, result)
    return result

# ---------------------------------------------------------
# ENGINE-INTEGRATED LOW-RAM WRAPPER
# ---------------------------------------------------------

def low_ram_run(text: str):
    """
    Android-safe wrapper around mvqueen_engine.engine.run().
    """
    from mvqueen_engine.engine import run
    return low_ram_process(text, run)

# ---------------------------------------------------------
# BATCH LOW-RAM PROCESSING
# ---------------------------------------------------------

def low_ram_batch(texts: list[str]):
    """
    Process many texts safely on Android.
    Uses caching and avoids RAM spikes.
    """
    results = []
    for t in texts:
        results.append(low_ram_run(t))
    return results