import json
import os

with open('HTbinning.json') as binning_file:    
    data = json.load(binning_file)

os.system('mkdir -p cards')
for process in data.keys():
    cmd = 'cp pythia.cmd cards/pythia_{}.cmd'.format(process)
    os.system(cmd)
