import json
import os, glob
import os.path

def writecards(binning, indir):
    
    incard = indir + '/run_card.dat'
    
    with open(incard) as f:
        infile = f.readlines()
        for i in xrange(1,len(binning)-1):
          if os.path.isdir("%sPT_%i_%i"%(indir,binning[i],binning[i+1]))==False:
            cmd="mkdir %sPT_%i_%i"%(indir,binning[i],binning[i+1])
            os.system(cmd)
            cmd='cp %sproc_card.dat %sPT_%i_%i'%(indir,indir,binning[i],binning[i+1])
            os.system(cmd)
          if os.path.isfile('%scuts.f'%(indir)):
            cmd='cp %scuts.f %sPT_%i_%i'%(indir,indir,binning[i],binning[i+1])
            os.system(cmd)
          if os.path.isfile('%scustomizecards.f'%(indir)):
            cmd='cp %scuts.f %sPT_%i_%i'%(indir,indir,binning[i],binning[i+1])
            os.system(cmd)
          if os.path.isfile('%sextramodels.f'%(indir)):
            cmd='cp %scuts.f %sPT_%i_%i'%(indir,indir,binning[i],binning[i+1])
            os.system(cmd)

          for line in xrange(len(infile)):
            if 'minimum pt for the jets' in infile[line] :
                infile[line]='%.1f = ptj  !minimum pt for the jets\n'%(binning[i])
            if 'maximum pt for the jets' in infile[line]:
                infile[line]='%.1f = ptjmax  !maximum pt for the jets\n'%(binning[i+1])
          with open("%sPT_%i_%i/run_card.dat"%(indir,binning[i],binning[i+1]), "w") as f1:
            f1.writelines(infile)        


def launchProcess(process, binning, indir, queue):
    
   for i in xrange(1,len(binning)-1):
     
     htdir="%sPT_%i_%i"%(indir,binning[i],binning[i+1])
     procht="{0}_PT_{1}_{2}".format(process, binning[i],binning[i+1])
     cmd="./gridpack_generation.sh {0} {1} {2}".format(procht, htdir, queue)
     #cmd="./submit_gridpack_generation.sh 15000 15000 1nd {0} {1} {2}".format(procht, htdir, queue)
     print cmd
     os.system(cmd)


def checkJobs(process, binning, queue):
    
   
   desc = binning[0][0]
   decay = binning[0][1]
   match = binning[0][2]
   kf = binning[0][3]
   
   stdouts = glob.glob('LSF*/STDOUT')
   #logs = glob.glob('*.log')
   #logs2 = glob.glob('logs/*.log')
   #logs3 = glob.glob('logs/LSF*/STDOUT')
   
   #logs = stdouts + logs + logs2 + logs3
   logs = stdouts
   
   import param2 as para
   
   for i in xrange(1,len(binning)-1):
     indir="cards/production/{0}/".format(process) 
     htdir="%sPT_%i_%i"%(indir,binning[i],binning[i+1])
     procht="{0}_PT_{1}_{2}".format(process, binning[i],binning[i+1])
     found = False
     print '----------------------------------------------------'
     print 'Checking process ...', procht
     
     #with open('param.py', 'a') as jf, open('process_list.txt', 'a') as lhejf, open('copyCards.sh', 'a') as cpeos :
     with open('param.py', 'a') as jf, open('process_list.txt', 'a') as lhejf, open('copyall.sh', 'a') as cpeos :
     
       lhejf.write("python sendJobs.py -n 100 -e 10000 -q 1nd -p {}\n".format(procht))
       #lhejf.write("sleep 3h\n")
       #lhejf.write("eos ls /eos/fcc/hh/generation/mg5_amcatnlo/gridpacks/{}.tar.gz\n".format(procht))
       #lhejf.write("ls {}.tar.gz\n".format(procht))
       #lhejf.write("sleep 3h\n")
       #lhejf.write("eos cp {}.tar.gz /eos/fcc/hh/generation/mg5_amcatnlo/gridpacks/{}.tar.gz\n".format(procht, procht))
       #lhejf.write("{}\n".format(procht))
       #cpeos.write("cp {}.tar.gz /eos/experiment/fcc/hh/generation/mg5_amcatnlo/gridpacks/{}.tar.gz\n".format(procht, procht))
       #cpeos.write("eos cp /eos/fcc/hh/pythiacards/pythia_{}.cmd /eos/fcc/hh/pythiacards/pythia_{}.cmd\n".format(procht, procht))
       data = {}
       for log in logs:
	 if os.path.exists(log) and 'Done' in open(log).read() and procht in open(log).read():
	   found=True
	   with open(log) as f:
             for line in f:
               if line.find('Cross-section'):
                 list_of_words = line.split()
                 if any("Cross-section" in s for s in list_of_words):
                    found=True
                    xsec = list_of_words[2]
                    print '   cross-section: ', xsec
                    data[procht] = ['', '', '', '', xsec, '']
                    #if procht not in para.gridpacklist:
                    jf.write("'{}':['{}','{} < PT < {}','{}','{}','{}','1.0'],\n".format(procht,desc,binning[i],binning[i+1],match,xsec,kf))
                    cpeos.write("cp {}.tar.gz /eos/experiment/fcc/hh/generation/mg5_amcatnlo/gridpacks/{}.tar.gz\n".format(procht, procht))
                    #lhejf.write("python sendJobs.py -n 100 -e 10000 -q 2nw -p {}\n".format(procht))


     if not found:
       cmd="./submit_gridpack_generation.sh 50000 50000 2nw {0} {1} {2}".format(procht, htdir, queue)
       print '   ... did not find cross section, resubmitting job...'
       print cmd
       os.system(cmd)


def checkJobsNoBinning(process, binning, queue):
   
   desc = binning[0][0]
   decay = binning[0][1]
   match = binning[0][2]
   kf = binning[0][3]

   stdouts = glob.glob('LSF*/STDOUT')
   #logs = glob.glob('*.log')
   #logs2 = glob.glob('logs/*.log')
   #logs3 = glob.glob('logs/LSF*/STDOUT')
   
   #logs = stdouts + logs + logs2 + logs3
   logs = stdouts
   
   indir="cards/production/{0}/".format(process) 
   procht=process
   print procht
   found = False
   print '----------------------------------------------------'
   print 'Checking process ...', procht
       
   #with open('param.py', 'a') as jf, open('copyCards.sh', 'a') as cpeos :
   with open('param.py', 'a') as jf:
     #cpeos.write("eos cp {}.tar.gz /eos/fcc/hh/generation/mg5_amcatnlo/gridpacks/{}.tar.gz\n".format(procht, procht))
     #cpeos.write("eos cp /eos/fcc/hh/pythiacards/pythia_{}.cmd /eos/fcc/hh/pythiacards/pythia_{}.cmd\n".format(procht, procht))
     data = {}
     for log in logs:
       if os.path.exists(log) and 'Done' in open(log).read() and str(procht) in open(log).read() and '_PT_' not in open(log).read():
         found=True
         with open(log) as f:
           for line in f:
             if line.find('Cross-section'):
               list_of_words = line.split()
               if any("Cross-section" in s for s in list_of_words):
                  found=True
                  xsec = list_of_words[2]
                  print '   cross-section: ', xsec
                  data[procht] = ['', '', '', '', xsec, '']
                  #json.dump(data, jf)
                  jf.write("'{}':['{}','inclusive','{}','{}','{}','1.0'],\n".format(procht,desc,match,xsec,kf))
                  #os.system('eos cp {}.tar.gz /eos/fcc/hh/generation/mg5_amcatnlo/gridpacks/{}.tar.gz'.format(procht, procht))


   if not found:
     cmd="./submit_gridpack_generation.sh 50000 50000 2nw {0} {1} {2}".format(procht, indir, queue)
     print '   ... did not find cross section, resubmitting job...'
     print cmd
     #os.system(cmd)


#__________________________________________________________
if __name__=="__main__":
    Dir = os.getcwd()
    
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option ('-b', '--binning',  help='binning file',
                       dest='binning',
                       default='')

    parser.add_option ('-q', '--queue',  help='queue',
                       dest='queue',
                       default='')

   
    (options, args) = parser.parse_args()
    binning   = options.binning
    queue     = options.queue
    
    with open(binning) as binning_file:    
        data = json.load(binning_file)

    os.system('rm process_list.txt')
    os.system('rm param.py')

    #lsfdirs = glob.glob('*.log')
    counter = 0
    for process, htlist in data.iteritems():
       inputdir="cards/production/{0}/".format(process)
       writecards(data[process], inputdir)
       
       #checkJobs(process, data[process], queue)
       #checkJobsNoBinning(process, data[process], queue)
       #print 'writing cards for processes: ', process
       #print 'lauching processes: ', process
       #launchProcess(process, data[process], inputdir, queue)
       #cmd="rm -rf {0}_*".format(process)
       #os.system(cmd)
       #print 'resubmitted', counter, 'jobs'

