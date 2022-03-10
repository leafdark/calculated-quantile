import math
from tempfile import NamedTemporaryFile
import shutil
import csv
import numpy as np
from threading import Lock

from constant import POOL_ID, POOL_VALUES, FILENAME, SEPARATE_CHARACTER, LIMIT_USING_FUNCTION

HEADERS = [POOL_ID, POOL_VALUES]
lock = Lock()


def update_or_create_pool(pool_id, pool_values):
    """
        Update or create data
        :param pool_id: numeric
        :param pool_values: arr
        :return: boolean
    """
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    pool_values.sort()

    with open(FILENAME, "r", newline='') as csvfile, tempfile:
        lock.acquire()
        reader = csv.DictReader(csvfile, fieldnames=HEADERS)
        writer = csv.DictWriter(tempfile, fieldnames=HEADERS)
        is_updated = False
        for row in reader:
            if row[POOL_ID] == str(pool_id):
                row[POOL_VALUES] = SEPARATE_CHARACTER.join(str(x) for x in pool_values)
                is_updated = True
            row = {POOL_ID: row[POOL_ID], POOL_VALUES: row[POOL_VALUES]}
            writer.writerow(row)
        if not is_updated:
            row = {POOL_ID: pool_id,
                   POOL_VALUES: SEPARATE_CHARACTER.join(str(x) for x in pool_values)}
            writer.writerow(row)
    shutil.move(tempfile.name, FILENAME)
    lock.release()
    return is_updated


def calculate_quantile(pool_id, percentile):
    """
        Calculate quantile
        :param pool_id: numeric
        :param percentile: float
        :return: dict
    """
    pool_values = []
    with open(FILENAME, "r", newline='') as csvfile:
        lock.acquire()
        reader = csv.DictReader(csvfile, fieldnames=HEADERS)
        for row in reader:
            if row[POOL_ID] == str(pool_id):
                pool_values = [int(x) for x in row[POOL_VALUES].split(SEPARATE_CHARACTER)]
                break
        lock.release()
    if not pool_values:
        return {
            "is_error": True,
            "msg": "Could not find poolValues by poolId...."
        }
    if len(pool_values) < LIMIT_USING_FUNCTION:
        if percentile == 100:
            return {
                "quantile": pool_values[-1],
                "size_arr": len(pool_values)
            }
        result = percentile / 100 * (len(pool_values) + 1)
        return {
            "quantile": pool_values[math.floor(result) - 1],
            "size_arr": len(pool_values)
        }
    return {
        "quantile": np.percentile(pool_values, percentile),
        "size_arr": len(pool_values)
    }
