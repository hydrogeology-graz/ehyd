from ehyd import read_ehyd

s = read_ehyd("data//N-Tagessummen-112086.csv")

import glob

fnames = glob.glob("data//Raab//*.csv")

for fname in fnames:
    s = read_ehyd(fname)
    # (s-s.mean()).plot()
    s.plot()
