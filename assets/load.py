"""Avgränsad last: fyra samtidiga klienter, högst fem minuter."""
import concurrent.futures
import time
from urllib.request import urlopen
from urllib.error import URLError

end = time.monotonic() + 300

def worker(_):
    successes = 0
    while time.monotonic() < end:
        try:
            with urlopen("http://web/work", timeout=10) as response:
                response.read()
                successes += 1
        except (URLError, TimeoutError):
            time.sleep(0.2)
    return successes

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(worker, range(4))), flush=True)
