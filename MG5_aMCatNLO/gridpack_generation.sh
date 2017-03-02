
#!/bin/bash

##########################################################################################
#GENERAL INSTRUCTIONS:                                                                   #
#You should take care of having the following ingredients in order to have this recipe   #
#working: run card and proc card (in a "cards" folder)                                   #
#all in the same folder!                                                                 #
#Important: Param card is not mandatory for this script                                  #
##########################################################################################


##########################################################################################
#For runnning, the following command should be used                                      #
#./create_gridpack_template.sh NAME_OF_PRODCUTION RELATIVE_PATH_TO_CARDS QUEUE_SELECTION #
#by NAME_OF_PRODUCTION you should use the names of run and proc card                     #
#for example if the cards are bb_100_250_proc_card_mg5.dat and bb_100_250_run_card.dat   #
#NAME_OF_PRODUCTION should be bb_100_250                                                 #
#for QUEUE_SELECTION is commonly used 1nd, but you can take another choice from bqueues  #
#If QUEUE_SELECTION is omitted, then run on local machine only (using multiple cores)    #
##########################################################################################

source /afs/cern.ch/sw/lcg/releases/LCG_86/gcc/4.9.3/x86_64-slc6/setup.sh
#source /afs/cern.ch/sw/lcg/releases/LCG_86/Boost/1.62.0/x86_64-slc6-gcc49-opt/Boost-env.sh

#source /afs/cern.ch/sw/lcg/releases/LCG_80/gcc/4.9.3/x86_64-slc6/setup.sh
#source /afs/cern.ch/sw/lcg/releases/LCG_80/Boost/1.59.0_python2.7/x86_64-slc6-gcc49-opt/Boost-env.sh

#source /cvmfs/sft.cern.ch/lcg/releases/LCG_87/gcc/4.9.3/x86_64-slc6/setup.sh
#source /cvmfs/sft.cern.ch/lcg/releases/LCG_87/Boost/1.62.0/x86_64-slc6-gcc49-opt/Boost-env.sh

#exit on first error
set -e

#First you need to set couple of settings:
name=${1}

# name of the run
carddir=${2}

# which queue
queue=${3}

if [ -z "$PRODHOME" ]; then
  PRODHOME=`pwd`
fi 

#catch unset variables
set -u

if [ -z ${name} ]; then
  echo "Process/card name not provided"
  if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
fi

if [ -z ${queue} ]; then
  queue=local
fi

#________________________________________
# to be set for user specific
# Release to be used to define the environment and the compiler needed

#For correct running you should place at least the run and proc card in a folder under the name "cards" in the same folder where you are going to run the script

RUNHOME=`pwd`

LOGFILE=${RUNHOME}/${name}.log
if [ "${name}" != "interactive" ]; then
  exec > >(tee ${LOGFILE})
  exec 2>&1
fi

echo "Starting job on " `date` #Only to display the starting of production date
echo "Running on " `uname -a` #Only to display the machine where the job is running
echo "System release " `cat /etc/redhat-release` #And the system release

echo "name: ${name}"
echo "carddir: ${carddir}"
echo "queue: ${queue}"

cd $PRODHOME

AFSFOLD=${PRODHOME}/${name}
# the folder where the script works, I guess
AFS_GEN_FOLDER=${RUNHOME}/${name}
# where to search for datacards, that have to follow a naming code: 
#   proc_card_mg5.dat
#   run_card.dat
CARDSDIR=${PRODHOME}/${carddir}
# where to find the madgraph tarred distribution


MGBASEDIR=mgbasedir

MG=MG5_aMC_v2.5.2.tar.gz
MGSOURCE=https://launchpad.net/mg5amcnlo/2.0/2.5.x/+download/$MG
#syscalc is a helper tool for madgraph to add scale and pdf variation weights for LO processes
SYSCALC=SysCalc_V1.1.6.tar.gz
SYSCALCSOURCE=https://cms-project-generators.web.cern.ch/cms-project-generators/$SYSCALC

MGBASEDIRORIG=MG5_aMC_v2_5_2

isscratchspace=0

if [ ! -d ${AFS_GEN_FOLDER}/${name}_gridpack ]; then
  #directory doesn't exist, create it and set up environment
  
  if [ ! -d ${AFS_GEN_FOLDER} ]; then
    mkdir ${AFS_GEN_FOLDER}
  fi

  cd $AFS_GEN_FOLDER


  ############################
  #Create a workplace to work#
  ############################
  
  mkdir -p ${name}_gridpack/work ; cd ${name}_gridpack/work
  WORKDIR=`pwd`

  #############################################
  #Copy, Unzip and Delete the MadGraph tarball#
  #############################################
  set +e
  wget --no-check-certificate ${MGSOURCE}
  if [ $? -ne 0 ]; then
    echo "Could not find release on central server, try locally"
    cp ${MGSOURCE_ALT} . 
  fi
  #set -e
  tar xzf ${MG}
  rm $MG

  ################################
  # Prepare MG input parameters 
  ################################
  
  cd $MGBASEDIRORIG
  
  ### need to patch makefile in SubProcesses ###
  wget https://raw.githubusercontent.com/selvaggi/GridPackProducer/master/MG5_aMCatNLO/patches/lhapdfFlags/makefile
  mv makefile Template/LO/SubProcesses/
  
  #LHAPDFCONFIG=/cvmfs/sft.cern.ch/lcg/releases/LCG_87/MCGenerators/lhapdf/6.1.6/x86_64-slc6-gcc49-opt/bin/lhapdf-config
  #LHAPDFCONFIG=/cvmfs/sft.cern.ch/lcg/releases/LCG_80/MCGenerators/lhapdf/6.1.5/x86_64-slc6-gcc49-opt/bin/lhapdf-config
  LHAPDFCONFIG=/cvmfs/sft.cern.ch/lcg/releases/LCG_86/MCGenerators/lhapdf/6.1.6/x86_64-slc6-gcc49-opt/bin/lhapdf-config
  #LHAPDFCONFIG=/cvmfs/sft.cern.ch/lcg/releases/LCG_86/MCGenerators/lhapdf/6.1.6.cxxstd/x86_64-slc6-gcc49-opt/bin/lhapdf-config
  #LHAPDFCONFIG=/afs/cern.ch/work/s/selvaggi/private/MG5_aMC_v2_5_2/HEPTools/lhapdf6/bin/lhapdf-config
  
  #make sure env variable forexit pdfsets points to the right place
  #export LHAPDF_DATA_PATH=/cvmfs/sft.cern.ch/lcg/external/lhapdfsets/current/:/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/lhapdf/6.1.6-77fe6/x86_64-slc6-gcc49-opt/share/LHAPDF
  #export LHAPDF_DATA_PATH=/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/lhapdf/6.1.6-77fe6/x86_64-slc6-gcc49-opt/share/LHAPDF
  #export LHAPDF_DATA_PATH=`$LHAPDFCONFIG --datadir`:$LHAPDF_DATA_PATH
  
  export LHAPDF_DATA_PATH=/cvmfs/sft.cern.ch/lcg/releases/LCG_87/MCGenerators/lhapdf/6.1.6/x86_64-slc6-gcc49-opt/share/LHAPDF:/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/lhapdf/6.1.6-77fe6/x86_64-slc6-gcc49-opt/share/LHAPDF
  #export LHAPDF_DATA_PATH=/afs/cern.ch/work/s/selvaggi/private/GridPackProducer/MG5_aMCatNLO/lhapdf_test
  #export LHAPDF_DATA_PATH=/afs/cern.ch/work/s/selvaggi/private/GridPackProducer/MG5_aMCatNLO/lhapdf_test:/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/lhapdf/6.1.6-77fe6/x86_64-slc6-gcc49-opt/share/LHAPDF
  
  #LHAPDF_DATA_PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/lhapdf/6.1.5/share/LHAPDF/
  #LHAPDFCONFIG=$LHAPDF_DATA_PATH/../../bin/lhapdf-config

  #LHAPDFCONFIG=/cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/lhapdf/6.1.6/bin/lhapdf-config
  #export LHAPDF_DATA_PATH= /cvmfs/cms.cern.ch/slc6_amd64_gcc493/external/lhapdf/6.1.6/share/LHAPDF

  echo "set auto_update 0" > mgconfigscript
  echo "set automatic_html_opening False" >> mgconfigscript
#  echo "set output_dependencies internal" >> mgconfigscript
  echo "set lhapdf $LHAPDFCONFIG" >> mgconfigscript
#   echo "set ninja $PWD/HEPTools/lib" >> mgconfigscript

  if [ "$queue" == "local" ]; then
      echo "set run_mode 2" >> mgconfigscript
  else
      #suppress lsf emails
      export LSB_JOB_REPORT_MAIL="N"

      echo "set run_mode  1" >> mgconfigscript
      if [ "$queue" == "condor" ]; then
        echo "set cluster_type condor" >> mgconfigscript
        echo "set cluster_queue None" >> mgconfigscript
      else
        echo "set cluster_type lsf" >> mgconfigscript
        echo "set cluster_queue $queue" >> mgconfigscript
      fi 
      echo "set cluster_status_update 60 30" >> mgconfigscript
      echo "set cluster_nb_retry 3" >> mgconfigscript
      echo "set cluster_retry_wait 300" >> mgconfigscript 
      echo "display options" >> mgconfigscript 
      
      #echo "set cluster_local_path `${LHAPDFCONFIG} --datadir`" >> mgconfigscript 
      if [[ ! "$RUNHOME" =~ ^/afs/.* ]]; then
          echo "local path is not an afs path, batch jobs will use worker node scratch space instead of afs"
          #*FIXME* broken in mg_amc 2.4.0
#           echo "set cluster_temp_path `echo $RUNHOME`" >> mgconfigscript 
          echo "set cluster_retry_wait 30" >> mgconfigscript 
          isscratchspace=1
      fi      
  fi

  echo "save options" >> mgconfigscript

  ./bin/mg5_aMC mgconfigscript

  ####################################
  # Access extra BSM models if needed
  ####################################
  
  MODELSDIR=${PRODHOME}/models

  #load extra models if needed
  if [ -e $CARDSDIR/extramodels.dat ]; then
    echo "Loading extra models specified in $CARDSDIR/extramodels.dat"
    #strip comments
    sed 's:#.*$::g' $CARDSDIR/extramodels.dat | while read model
    do
      #get needed BSM model
      if [[ $model = *[!\ ]* ]]; then
        echo ${MODELSDIR}/${model}
        if [[ -e ${MODELSDIR}/${model} ]]; then
          echo "Loading extra model $model"
          cp ${MODELSDIR}/${model} .
          cd models
          if [[ $model == *".zip"* ]]; then
            unzip ../$model
          elif [[ $model == *".tgz"* ]]; then
            tar zxvf ../$model
          elif [[ $model == *".tar"* ]]; then
            tar xavf ../$model
          else 
            echo "A BSM model is specified but it is not in a standard archive (.zip or .tar)"
          fi
          cd ..
        else
          echo "BSM model specified in $CARDSDIR/extramodels.dat does not match any model in extramodels
          directory."
          if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
        fi
      fi
    done
  fi

  cd $WORKDIR
  
  if [ "$name" == "interactive" ]; then
    set +e
    set +u
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 0; else exit 0; fi
  fi

  echo `pwd`


  if [ -z ${carddir} ]; then
    echo "Card directory not provided"
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi

  if [ ! -d $CARDSDIR ]; then
    echo $CARDSDIR " does not exist!"
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi  
  
  ########################
  #Locating the proc card#
  ########################
  if [ ! -e $CARDSDIR/proc_card.dat ]; then
    echo $CARDSDIR/proc_card.dat " does not exist!"
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi

  if [ ! -e $CARDSDIR/run_card.dat ]; then
    echo $CARDSDIR/run_card.dat " does not exist!"
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi  
  
  cp $CARDSDIR/proc_card.dat proc_card.dat
  echo "output ${name}" >> proc_card.dat


  ########################
  #Run the code-generation step to create the process directory
  ########################

  ./$MGBASEDIRORIG/bin/mg5_aMC proc_card.dat

  #*FIXME* workaround for broken set cluster_queue handling (only needed for LSF)
  if [ "$queue" != "condor" ]; then
    echo "cluster_queue = $queue" >> ./$MGBASEDIRORIG/input/mg5_configuration.txt
  fi
  if [ "$isscratchspace" -gt "0" ]; then
    echo "cluster_temp_path = `echo $RUNHOME`" >> ./$MGBASEDIRORIG/input/mg5_configuration.txt
  fi
#   echo "cluster_local_path = `${LHAPDFCONFIG} --datadir`" >> ./$MGBASEDIRORIG/input/mg5_configuration.txt    
  
  if [ -e $CARDSDIR/patch_me.sh ]; then
      echo "Patching generated matrix element code with " $CARDSDIR/patch_me.sh
      /bin/bash "$CARDSDIR/patch_me.sh" "$WORKDIR/$MGBASEDIRORIG"
  fi;
  
else  
  echo "Reusing existing directory assuming generated code already exists"
  echo "WARNING: If you changed the process card you need to clean the folder and run from scratch"
  
  cd $AFS_GEN_FOLDER
  
  WORKDIR=$AFS_GEN_FOLDER/${name}_gridpack/work/
  if [ ! -d ${WORKDIR} ]; then
    echo "Existing directory does not contain expected folder $WORKDIR"
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi
  cd $WORKDIR


  if [ "$name" == "interactive" ]; then
    set +e
    set +u  
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 0; else exit 0; fi
  else
    echo "Reusing an existing process directory ${name} is not actually supported in production at the moment.  Please clean or move the directory and start from scratch."
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi
  
  if [ -z ${carddir} ]; then
    echo "Card directory not provided"
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi

  if [ ! -d $CARDSDIR ]; then
    echo $CARDSDIR " does not exist!"
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi
  
  if [ ! -e $CARDSDIR/run_card.dat ]; then
    echo $CARDSDIR/run_card.dat " does not exist!"
    if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
  fi  

fi  

if [ -d gridpack ]; then
  rm -rf gridpack
fi

if [ -d processtmp ]; then
  rm -rf processtmp
fi

if [ -d process ]; then
  rm -rf process
fi

if [ ! -d ${name} ]; then
  echo "Process output directory ${name} not found.  Either process generation failed, or the name of the output did not match the process name ${name} provided to the script."
  if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 1; else exit 1; fi
fi

#make copy of process directory for reuse only if not running on temp scratch space
if [ "$isscratchspace" -gt "0" ]; then
  echo "moving generated process to working directory"
  mv $name processtmp
else
  echo "copying generated process to working directory"
  cp -a $name/ processtmp
fi

cd processtmp

#######################
#Locating the run card#
#######################

echo "copying run_card.dat file"
cp $CARDSDIR/run_card.dat ./Cards/run_card.dat

#copy provided custom fks params or cuts
if [ -e $CARDSDIR/cuts.f ]; then
  echo "copying custom cuts.f file"
  cp $CARDSDIR/cuts.f ./SubProcesses/cuts.f
fi

if [ -e $CARDSDIR/FKS_params.dat ]; then
  echo "copying custom FKS_params.dat file"
  cp $CARDSDIR/FKS_params.dat ./Cards/FKS_params.dat
fi

if [ -e $CARDSDIR/setscales.f ]; then
  echo "copying custom setscales.f file"
  cp $CARDSDIR/setscales.f ./SubProcesses/setscales.f
fi

if [ -e $CARDSDIR/reweight_xsec.f ]; then
  echo "copying custom reweight_xsec.f file"
  cp $CARDSDIR/reweight_xsec.f ./SubProcesses/reweight_xsec.f
fi

if [ -e $CARDSDIR/reweight_card.dat ]; then
  echo "copying custom reweight file"
  cp $CARDSDIR/reweight_card.dat ./Cards/reweight_card.dat
fi


#automatically detect NLO mode or LO mode from output directory
isnlo=0
if [ -e ./MCatNLO ]; then
  isnlo=1
fi

if [ "$isnlo" -gt "0" ]; then
#NLO mode  
  #######################
  #Run the integration and generate the grid
  #######################

  if [ -e $CARDSDIR/madspin_card.dat ]; then
    cp $CARDSDIR/madspin_card.dat ./Cards/madspin_card.dat
  fi
  
  echo "shower=OFF" > makegrid.dat
  echo "done" >> makegrid.dat
  if [ -e $CARDSDIR/customizecards.dat ]; then
          cat $CARDSDIR/customizecards.dat >> makegrid.dat
          echo "" >> makegrid.dat
  fi
  echo "done" >> makegrid.dat

  cat makegrid.dat | ./bin/generate_events -n pilotrun

  if [ -e $CARDSDIR/externaltarball.dat ]; then
      gunzip ./Events/pilotrun_decayed_1/events.lhe.gz
      sed -n '/<MG5ProcCard>/,/<\/slha>/p' ./Events/pilotrun_decayed_1/events.lhe > header_for_madspin.txt
      mv header_for_madspin.txt $WORKDIR
      gzip ./Events/pilotrun_decayed_1/events.lhe
  fi
  
  echo "mg5_path = ../mgbasedir" >> ./Cards/amcatnlo_configuration.txt
#   echo "ninja = ../mgbasedir/HEPTools/lib" >> ./Cards/amcatnlo_configuration.txt
  echo "cluster_temp_path = None" >> ./Cards/amcatnlo_configuration.txt

  cd $WORKDIR
  
  mkdir gridpack

  mv processtmp gridpack/process

  cp -a $MGBASEDIRORIG/ gridpack/mgbasedir
  
  cd gridpack
  
  if [ -e $CARDSDIR/externaltarball.dat ]; then
    mv $WORKDIR/header_for_madspin.txt . 
  fi
  
else
  #LO mode
  #######################
  #Run the integration and generate the grid
  #######################
  
  echo "done" > makegrid.dat
  echo "set gridpack True" >> makegrid.dat
  if [ -e $CARDSDIR/customizecards.dat ]; then
          cat $CARDSDIR/customizecards.dat >> makegrid.dat
          echo "" >> makegrid.dat
  fi
  echo "done" >> makegrid.dat

#   set +e
  cat makegrid.dat | ./bin/generate_events pilotrun

  cd $WORKDIR
    
  echo "cleaning temporary output"
  mv $WORKDIR/processtmp/pilotrun_gridpack.tar.gz $WORKDIR/
  mv $WORKDIR/processtmp/Events/pilotrun/unweighted_events.lhe.gz $WORKDIR/
  rm -rf processtmp
  mkdir process
  cd process
  echo "unpacking temporary gridpack"
  tar -xzf $WORKDIR/pilotrun_gridpack.tar.gz
  echo "cleaning temporary gridpack"
  rm $WORKDIR/pilotrun_gridpack.tar.gz
  
  # precompile reweighting if necessary
  if [ -e $CARDSDIR/reweight_card.dat ]; then
      pwd
      echo "preparing reweighting step"
      mkdir -p madevent/Events/pilotrun
      cp $WORKDIR/unweighted_events.lhe.gz madevent/Events/pilotrun
      echo "f2py_compiler=" `which gfortran` >> ./madevent/Cards/me5_configuration.txt
      #need to set library path or f2py won't find libraries
      export LIBRARY_PATH=$LD_LIBRARY_PATH
      cd madevent
      bin/madevent reweight pilotrun
      # Explicitly compile all subprocesses
      for file in $(ls -d rwgt/*/SubProcesses/P*); do
        echo "Compiling subprocess $(basename $file)"
        cd $file
        for i in 2 3; do
            MENUM=$i make matrix${i}py.so >& /dev/null
            echo "Library MENUM=$i compiled with status $?"
        done
        cd -
      done
      cd ..      
  fi
  
  #prepare madspin grids if necessary
  if [ -e $CARDSDIR/madspin_card.dat ]; then
    echo "import $WORKDIR/unweighted_events.lhe.gz" > madspinrun.dat
    cat $CARDSDIR/madspin_card.dat >> madspinrun.dat
    cat madspinrun.dat | $WORKDIR/$MGBASEDIRORIG/MadSpin/madspin
    rm madspinrun.dat
    rm -rf tmp*
    cp $CARDSDIR/madspin_card.dat $WORKDIR/process/madspin_card.dat
  fi

  echo "preparing final gridpack"
  
  #set to single core mode
  echo "mg5_path = ../../mgbasedir" >> ./madevent/Cards/me5_configuration.txt
  echo "cluster_temp_path = None" >> ./madevent/Cards/me5_configuration.txt
  echo "run_mode = 0" >> ./madevent/Cards/me5_configuration.txt  
    
  cd $WORKDIR
  
  mkdir gridpack
  mv process gridpack/process
  cp -a $MGBASEDIRORIG/ gridpack/mgbasedir

  cd gridpack
  
fi

#clean unneeded files for generation
$PRODHOME/cleangridpack.sh

#
#Plan to decay events from external tarball?
# 

if [ -e $CARDSDIR/externaltarball.dat ]; then
    echo "Locating the external tarball"
    cp $CARDSDIR/externaltarball.dat .
    source $CARDSDIR/externaltarball.dat
    echo $EXTERNAL_TARBALL 
    cp $EXTERNAL_TARBALL .
    tarname=$(basename $EXTERNAL_TARBALL)
    mkdir external_tarball
    cd external_tarball
    tar -xvaf ../$tarname
    cd ..
    rm $tarname
fi


echo "Saving log file"
#copy log file
cp ${LOGFILE} ./gridpack_generation.log

echo "Creating tarball"

if [ ! -e $CARDSDIR/externaltarball.dat ]; then
    tar -czvf ${name}.tar.gz mgbasedir process gridpack_generation.log
else
    tar -czvf ${name}.tar.gz mgbasedir process gridpack_generation.log external_tarball ${name}_externaltarball.dat header_for_madspin.txt
fi

mv ${name}.tar.gz ${PRODHOME}/${name}.tar.gz

echo "Gridpack created successfully at ${PRODHOME}/${name}.tar.gz"
echo "End of job"

if [ "${BASH_SOURCE[0]}" != "${0}" ]; then return 0; else exit 0; fi
