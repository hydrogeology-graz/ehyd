import urllib
import os
import time
import numpy as np

# 329557
for i in range(329557, 329559):  # too large range for one go
    filename = 'GW_monatsmittel_{0}.csv'.format(i)
    url = 'http://ehyd.gv.at/eHYD/MessstellenExtraData/gw?id={0}&file=4'.format(
        i)
    urllib.request.urlretrieve(url, filename)
    if os.path.getsize(filename) == 0:
        os.remove(filename)
    time.sleep(np.random.rand() / 2)
