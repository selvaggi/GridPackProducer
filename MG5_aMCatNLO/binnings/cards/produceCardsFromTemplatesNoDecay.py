import json
import os

with open('../HTbinning_higgs_v5.json') as binning_file:    
    data = json.load(binning_file)

os.system('mkdir -p cards_higgs')
cpeos = open('copyCardsOnEos.sh', 'w')

nmax = 20000

eospath='/eos/experiment/fcc/hh/utils/pythiacards/'
evprod_path='/afs/cern.ch/work/s/selvaggi/private/EventProducer'

subjobs = open('{}/submitJobs.sh'.format(evprod_path), 'w')

for process in data.keys():
    
    binning = data[process]
    bins = []
    
    template = 'pythia_{}.cmd'.format(process)
    
    for i in xrange(1,len(binning)-1):
        bins.append('HT_{}_{}'.format(binning[i],binning[i+1]))

    # binned inclusive processes
    for b in bins:
        
	
	card_i = '{}/pythia_{}.cmd'.format(eospath,process)
	card_f = '{}/pythia_{}_{}.cmd'.format(eospath,process, b)

        cmd = 'cp {} {}'.format(card_i, card_f)
	
	#fc.write('cp {} {}\n'.format(template, dest))
        cpeos.write('{}\n'.format(cmd))
        subjobs.write('python bin/sendJobs_FCCSW.py -n 100 -p {}_{} -q 8nh -v fcc_v02\n'.format(process, b))
