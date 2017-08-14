#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/releases/LCG_88/gcc/4.9.3/x86_64-slc6/setup.sh

nevt=${1}
echo "%MSG-MG5 number of events requested = $nevt"

rnum=${2}
echo "%MSG-MG5 random seed used for the run = $rnum"

LHEWORKDIR=`pwd`

cd $LHEWORKDIR

LHAPDFCONFIG=/afs/cern.ch/work/s/selvaggi/public/LHAPDF-6.1.6/build/bin/lhapdf-config
export LHAPDF_DATA_PATH=/afs/cern.ch/work/s/selvaggi/public/LHAPDF-6.1.6/build/share/LHAPDF

echo "lhapdf = $LHAPDFCONFIG" >> ./Cards/amcatnlo_configuration.txt
# echo "cluster_local_path = `${LHAPDFCONFIG} --datadir`" >> ./Cards/amcatnlo_configuration.txt

echo "run_mode = 0" >> ./Cards/amcatnlo_configuration.txt

echo "done" > runscript.dat
echo "set nevents ${nevt}" >> runscript.dat
echo "set iseed ${rnum}" >> runscript.dat

echo "done" >> runscript.dat

echo "${nevt} = nevents " >> ./Cards/run_card.dat
echo "${rnum} = iseed " >> ./Cards/run_card.dat

runname=cmsgrid

#generate events

#First check if normal operation with MG5_aMCatNLO events is planned

#cat runscript.dat | ./bin/generate_events -ox -n $runname
cat runscript.dat | ./bin/generate_events -f -p --nocompile --only_generation -n $runname

mv ./Events/${runname}/events.lhe.gz $LHEWORKDIR

cd $LHEWORKDIR
gzip -d events.lhe.gz

ls -l
echo

exit 0
