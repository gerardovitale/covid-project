import functools
from time import perf_counter


def time_it(method):
    @functools.wraps(method)
    def timed(*args, **kw):
        result = None
        start_time = perf_counter()
        try:
            result = method(*args, **kw)
        except Exception as exc:
            exception = exc
            raise exc from None
        finally:
            end_time = perf_counter()
            result_time = (end_time - start_time) * 1000
            print('[INFO] Time consumed: {0} {1:.6f} ms'.format(method.__name__, result_time))
        return result

    return timed
