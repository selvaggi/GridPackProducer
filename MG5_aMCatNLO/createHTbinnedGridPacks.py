import json
import os

def writecards(binning, indir):
    
    incard = indir + '/run_card.dat'
    
    with open(incard) as f:
        infile = f.readlines()
        for i in xrange(0,len(binning)-1):
          if os.path.isdir("%sHT_%i_%i"%(indir,binning[i],binning[i+1]))==False:
            cmd="mkdir %sHT_%i_%i"%(indir,binning[i],binning[i+1])
            os.system(cmd)
            cmd='cp %sproc_card.dat %sHT_%i_%i'%(indir,indir,binning[i],binning[i+1])
            os.system(cmd)
          if os.path.isfile('%scuts.f'%(indir)):
            cmd='cp %scuts.f %sHT_%i_%i'%(indir,indir,binning[i],binning[i+1])
            os.system(cmd)
          if os.path.isfile('%scustomizecards.f'%(indir)):
            cmd='cp %scuts.f %sHT_%i_%i'%(indir,indir,binning[i],binning[i+1])
            os.system(cmd)
          if os.path.isfile('%sextramodels.f'%(indir)):
            cmd='cp %scuts.f %sHT_%i_%i'%(indir,indir,binning[i],binning[i+1])
            os.system(cmd)

          for line in xrange(len(infile)):
            if 'ihtmin' in infile[line] :
                infile[line]='%.1f = ihtmin  !inclusive Ht for all partons (including b)\n'%(binning[i])
            if 'ihtmax' in infile[line]:
                infile[line]='%.1f = ihtmax  !inclusive Ht for all partons (including b)\n'%(binning[i+1])
          with open("%sHT_%i_%i/run_card.dat"%(indir,binning[i],binning[i+1]), "w") as f1:
            f1.writelines(infile)        


def launchProcess(process, binning, indir, queue):
    
   for i in xrange(0,len(binning)-1):
     
     htdir="%sHT_%i_%i"%(indir,binning[i],binning[i+1])
     procht="{0}_HT_{1}_{2}".format(process, binning[i],binning[i+1])
     #cmd="./gridpack_generation.sh {0} {1} {2}".format(procht, htdir, queue)
     cmd="./submit_gridpack_generation.sh 15000 15000 1nd {0} {1} {2}".format(procht, htdir, queue)
     print cmd
     os.system(cmd)

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
                       default='8nh')
   
    (options, args) = parser.parse_args()
    binning   = options.binning
    queue     = options.queue
    
    with open(binning) as binning_file:    
        data = json.load(binning_file)

    for process, htlist in data.iteritems():
       print 'writing cards for processes: ', process
       inputdir="cards/production/{0}/".format(process)
       writecards(data[process], inputdir)
       print 'lauching processes: ', process
       launchProcess(process, data[process], inputdir, queue)
