import json
import os, glob
import os.path

#___________________________________________________________________________________________________
def launchProcess(process, indir, queue_master, queue_daughter):

    cmd="./submit_gridpack_generation.sh 50000 50000 {} {} {} {}".format(queue_master, process, indir, queue_daughter)
    print cmd
    os.system(cmd)

#__________________________________________________________________________________________________
def checkJob(process, indir, queue_master, queue_daughter):

   stdouts = glob.glob('LSF*/STDOUT')
   logs = stdouts
   
   found = False
   print '----------------------------------------------------'
   print 'Checking process ...', process
     
   for log in logs:
     if os.path.exists(log) and 'Done' in open(log).read() and str(process) in open(log).read():
       with open(log) as f:
         for line in f:
           if line.find('Cross-section'):
             list_of_words = line.split()
             if any("Cross-section" in s for s in list_of_words):
                found=True
                xsec = list_of_words[2]
                print '   cross-section: ', xsec

   if found:
      return True

   else:
     print 'did not find process cross-section in log files, resubmitting {}'.format(process)
     launchProcess(process, indir, queue_master, queue_daughter)
     return False

#__________________________________________________________________________________________________
def writeOutput(process):

   print '----------------------------------------------------'
   print 'writing process ...', process

   stdouts = glob.glob('LSF*/STDOUT')
   logs = stdouts

   paramFile = 'param.py'

   with open(paramFile, 'a') as jf:
     for log in logs:
       if os.path.exists(log) and 'Done' in open(log).read() and str(process) in open(log).read():
         with open(log) as f:
           for line in f:
             if line.find('Cross-section'):
               list_of_words = line.split()
               if any("Cross-section" in s for s in list_of_words):
                  xsec = list_of_words[2]
                  print '   cross-section: ', xsec
                  jf.write("'{}':['','inclusive','','{}','1.0','1.0'],\n".format(process,xsec))

   #cmd = 'cp {}.tar.gz /eos/experiment/fcc/hh/generation/mg5_amcatnlo/gridpacks/{}.tar.gz'.format(process, process)
  
   eoscpscript='/afs/cern.ch/work/h/helsens/public/FCCutils/eoscopy.py'


   #cmd = 'cp {}.tar.gz /eos/experiment/fcc/helhc/generation/gridpacks/{}.tar.gz'.format(process, process)
   cmd = 'python {} {}.tar.gz /eos/experiment/fcc/hh/generation/mg5_amcatnlo/gridpacks/{}.tar.gz'.format(eoscpscript, process, process)
   print cmd
   os.system(cmd)


#__________________________________________________________
if __name__=="__main__":
    Dir = os.getcwd()
    
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option ('--plist',  help='process list file',
                       dest='plist',
                       default='lists/list.txt')

    parser.add_option ('--qm',  help='queue master',
                       dest='queue_master',
                       default='2nw')

    parser.add_option ('--qd',  help='queue daughter',
                       dest='queue_daughter',
                       default='1nd')
   
    parser.add_option("-c","--collect", help="collects gridpacks and cross sections",
                      dest="collect", action="store_true", 
                      default=False)

    parser.add_option("-l","--launch", help="launch gridpack production",
                      dest="launch", action="store_true", 
                      default=False)


    (options, args)  = parser.parse_args()
    queue_master     = options.queue_master
    queue_daughter   = options.queue_daughter
    collect          = options.collect
    launch           = options.launch
    plist            = options.plist

    os.system('rm process_list.txt')
    os.system('rm param.py')

    procList = [line.rstrip('\n') for line in open(plist)]

    counter = 0
    for inputdir in procList:

       process = os.path.basename(inputdir) 
       print process
       if launch:
           launchProcess(process, inputdir, queue_master, queue_daughter)
       
       if collect:
           if checkJob(process, inputdir, queue_master, queue_daughter):
	       counter +=1

    # if all jobs are done 
    if len(procList) == counter:
       for process in procList:
           process = os.path.basename(process)
           writeOutput(process)
