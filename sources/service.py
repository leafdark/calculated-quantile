import math
from tempfile import NamedTemporaryFile
import shutil
import csv
import numpy as np
from threading import Lock


filename = "pools_data.csv"

POOL_ID = 'poolId'
POOL_VALUES = 'poolValues'
SEPARATE_CHARACTER = '|'
HEADERS = [POOL_ID, POOL_VALUES]
LIMIT_USING_FUNCTION = 100
lock = Lock()


def update_or_create_pool(data):
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    pool_values = data.get(POOL_VALUES)
    pool_values.sort()

    with open(filename, "r", newline='') as csvfile, tempfile:
        lock.acquire()
        reader = csv.DictReader(csvfile, fieldnames=HEADERS)
        writer = csv.DictWriter(tempfile, fieldnames=HEADERS)
        is_updated = False
        for row in reader:
            if row[POOL_ID] == str(data.get(POOL_ID)):
                row[POOL_VALUES] = SEPARATE_CHARACTER.join(str(x) for x in pool_values)
                is_updated = True
            row = {POOL_ID: row[POOL_ID], POOL_VALUES: row[POOL_VALUES]}
            writer.writerow(row)
        if not is_updated:
            row = {POOL_ID: data.get(POOL_ID),
                   POOL_VALUES: SEPARATE_CHARACTER.join(str(x) for x in pool_values)}
            writer.writerow(row)
    shutil.move(tempfile.name, filename)
    lock.release()
    return is_updated


def calculate_quantile(data):
    with open(filename, "r", newline='') as csvfile:
        lock.acquire()
        reader = csv.DictReader(csvfile, fieldnames=HEADERS)
        pool_values = []
        for row in reader:
            if row[POOL_ID] == str(data.get(POOL_ID)):
                pool_values = [int(x) for x in row[POOL_VALUES].split(SEPARATE_CHARACTER)]
                break
        lock.release()
        if not pool_values:
            return {
                "is_error": True,
                "msg": "Could not find poolValues by poolId...."
            }
        if len(pool_values) < LIMIT_USING_FUNCTION:
            if data.get('percentile') == 100:
                return {
                    "quantile": pool_values[-1],
                    "size_arr": len(pool_values)
                }
            result = data.get('percentile') / 100 * (len(pool_values) + 1)
            return {
                "quantile": pool_values[math.floor(result) - 1],
                "size_arr": len(pool_values)
            }
        return {
            "quantile": np.percentile(pool_values, data.get('percentile')),
            "size_arr": len(pool_values)
        }
