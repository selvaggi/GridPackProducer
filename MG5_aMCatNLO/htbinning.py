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

            
          for line in xrange(len(infile)):
            if 'ihtmin' in infile[line] :
                infile[line]='%.1f = ihtmin  !inclusive Ht for all partons (including b)\n'%(binning[i])
            if 'ihtmax' in infile[line]:
                infile[line]='%.1f = ihtmax  !inclusive Ht for all partons (including b)\n'%(binning[i+1])
          with open("%sHT_%i_%i/run_card.dat"%(indir,binning[i],binning[i+1]), "w") as f1:
            f1.writelines(infile)        
#__________________________________________________________
if __name__=="__main__":
    Dir = os.getcwd()
    
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option ('-i','--inputdir', help='input process dir',
                       dest='inputdir',
                       default='')

    parser.add_option ('-b', '--binning',  help='binning file',
                       dest='binning',
                       default='')

    (options, args) = parser.parse_args()
    inputdir  = options.inputdir
    binning   = options.binning
     
    process = os.path.split(os.path.abspath(inputdir))[1]

    with open(binning) as binning_file:    
        data = json.load(binning_file)
    print data[process]
    
    writecards(data[process], inputdir)
