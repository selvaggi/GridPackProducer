import json
import os

with open('../HTbinning_vjets.json') as binning_file:    
    data = json.load(binning_file)


decays = ['zll', 'wlv']
signals = ['pp_w0123j_4f', 'pp_z0123j_4f']

os.system('mkdir -p cards')
fc = open('produceCards.sh', 'w')
cpeos = open('copyCardsOnEos.sh', 'w')
subjobs = open('submitJobs.sh', 'w')

nmax = 20000

for process in data.keys():
    
    print process
    binning = data[process]
    bins = []
    
    template = 'pythia_{}.cmd'.format(process)
    
    for i in xrange(1,len(binning)-1):
        bins.append('HT_{}_{}'.format(binning[i],binning[i+1]))

    # unbinned inclusive processes
    dest = 'cards/pythia_{}.cmd'.format(process)
    desteos = 'pythia_{}.cmd'.format(process)

    fc.write('cp {} {}\n'.format(template, dest))
    cpeos.write('cp {} /eos/experiment/fcc/hh/pythiacards/{}\n'.format(dest, desteos))
    subjobs.write('python bin/sendJobs_FCCSW.py -n 10000 -i {} -p {} -q 2nw -e -1\n'.format(nmax, process))
    
    # binned inclusive processes
    for b in bins:
        
	print b
	dest = 'cards/pythia_{}_{}.cmd'.format(process, b)
	desteos = 'pythia_{}_{}.cmd'.format(process, b)
        fc.write('cp {} {}\n'.format(template, dest))
        cpeos.write('cp {} /eos/experiment/fcc/hh/pythiacards/{}\n'.format(dest, desteos))
        subjobs.write('python bin/sendJobs_FCCSW.py -n 10000 -i {} -p {}_{} -q 2nw -e -1\n'.format(nmax, process, b))

    # decays for unbinned processes
    if process in signals:
        for decay in decays:
            
            dest = 'cards/pythia_{}_{}.cmd'.format(process, decay)
            desteos = 'pythia_{}_{}.cmd'.format(process, decay)
            fc.write('cp {} {}\n'.format(template, dest))
            cpeos.write('cp {} /eos/experiment/fcc/hh/pythiacards/{}\n'.format(dest, desteos))
            subjobs.write('python bin/sendJobs_FCCSW.py -n 10000 -i {} -p {} -q 2nw -e -1 -d {}\n'.format(nmax, process, decay))
            
            decay_main = 'cards/pythia_{}_{}.cmd'.format(process, decay)
            decay_file = '{}.cmd'.format(decay)
            
            fc.write('cat {} >> {}\n'.format(decay_file, decay_main))
            
            # decays for binned processes
            for b in bins:
		dest = 'cards/pythia_{}_{}_{}.cmd'.format(process, b, decay)
		desteos = 'pythia_{}_{}_{}.cmd'.format(process, b, decay)
                fc.write('cp {} {}\n'.format(decay_main, dest))
                cpeos.write('cp {} /eos/experiment/fcc/hh/pythiacards/{}\n'.format(dest, desteos))
                subjobs.write('python bin/sendJobs_FCCSW.py -n 10000 -i {} -p {}_{} -q 2nw -e -1 -d {}\n'.format(nmax, process, b, decay))
