import os, sys
import numpy as np

#___________________________________________
def decay_string(m_neut):
    neut_str = '{}'.format(m_neut)
    neut_str = neut_str.replace('.','p')
    br_str = decay_name.replace('YYY',neut_str)
    return br_str

#___________________________________________
def write_param(stop_masses, neutralino_masses, param_file):

    branching_str = '{\n'
    decay_str = '{\n'

    for m_neut in neutralino_masses:

        br_str = decay_string(m_neut)
        br_str = "'{}':1.0,\n".format(br_str)
        branching_str += br_str

    branching_str += '}\n'

    for m_stop in stop_masses:

        # here do full grid
        stop_str = '{}'.format(m_stop)

        dec_str = proc_name.replace('XXX',stop_str)
        dec_str = "'{}':[".format(dec_str)

        i = 0
        for m_neut in neutralino_masses:

            if m_neut > m_stop:
                continue
            #print m_stop, m_neut

            substr = decay_string(m_neut)
            #print substr

            if i > 0:
                substr = ",'{}'".format(substr)
            else:
                substr = "'{}'".format(substr)

            dec_str += substr

            #print dec_str

            i += 1

        dec_str += '],\n'

        decay_str += dec_str

    decay_str += '}\n'

    param_file.write(branching_str)
    param_file.write(decay_str)


#____________________________________________________________________________
def write_pythia_cards(templateCard, stop_masses, neutralino_masses):

    # read pythia8 template
    with open (templateCard, "r") as myfile:
        tempdata=myfile.readlines()


    cpOnEos = open('{}/cpOnEos.sh'.format(output_dir), 'w')

    for m_stop in stop_masses:

        # here do full grid
        stop_str = '{}'.format(m_stop)

        proc_str = proc_name.replace('XXX',stop_str)
        proc_str = proc_str.replace('mg_','')

        i = 0
        for m_neut in neutralino_masses:

            if m_neut > m_stop:
                continue

            dec_str = decay_string(m_neut)

            card_name = 'p8_{}_{}.cmd'.format(proc_str,dec_str)

            params = pythia_params.replace('MSTOP',str(m_stop*1000.))
            params = params.replace('MNEUT',str(m_neut*1000.))

            # write pythia8 card
            pythia_file = '{}/{}'.format(output_dir, card_name)
            pythia_card = open(pythia_file, 'w')
            for line in tempdata:
                pythia_card.write(line)
            pythia_card.write(params)

            # copy cards on eos
            cmd = 'python {} {} {}/{}\n'.format(eoscp, pythia_file, eosdest, card_name)
            cpOnEos.write(cmd)
	    
    print "pythia8 cards done ... To copy on eos, run:"
    print ''
    print '    source {}/cpOnEos.sh'.format(output_dir)
    print ''
    

#___________________________________________

templateCard = sys.argv[1]

eosdest = '/eos/experiment/fcc/hh/utils/pythiacards'
eoscp = '/afs/cern.ch/work/h/helsens/public/FCCutils/eoscopy.py'

proc_name = 'mg_pp_stopstop_5f_mStop_XXXTeV'
decay_name = 'mChi_YYYTeV'

# outputs
output_dir = 'stop_cards'
if not os.path.exists(output_dir):
     os.makedirs(output_dir)

param_file = open('{}/param.py'.format(output_dir), 'w')

# stop masses from 1 TeV to 11TeV with steps of 1TeV
stop_masses = np.arange(1,12)

# neutralino masses from 1 TeV to 11TeV with steps of 1TeV
neutralino_masses = np.arange(0.5,11.5, 1.)

# pythiacard chunk

pythia_params = '''
SLHA:readFrom = 0

! stop parameters
1000006:m0 = MSTOP
1000006:mWidth = 1.

! neutralino parameters
1000022:m0 = MNEUT
1000022:mWidth = 0.
1000022:onMode = off

! activate stop -> top neutralino and off-shell stop decays
1000006:onMode = off
1000006:11:onMode = on
1000006:11:bRatio = 1.
1000006:11:meMode = 100

1000006:addChannel = 1   0.0000000  100  1000022        5       24 
'''


# write param_file
write_param(stop_masses, neutralino_masses, param_file)

# write pythia cards
write_pythia_cards(templateCard, stop_masses, neutralino_masses)

