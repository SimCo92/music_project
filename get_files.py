from os import listdir
from os.path import isfile, join
import pandas

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

onlyfiles.tocsv("x.csv")

