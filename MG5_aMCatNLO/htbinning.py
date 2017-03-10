import json
import os

def writecards(binning, incard):
    outdir=incard.replace("run_card.dat","")
    with open(incard) as f:
        infile = f.readlines()
    for i in xrange(0,len(binning)-1):
        if os.path.isdir("%sHTbinning%i_%i"%(outdir,binning[i],binning[i+1]))==False:
            cmd="mkdir %sHTbinning%i_%i"%(outdir,binning[i],binning[i+1])
            os.system(cmd)
            cmd='cp %sproc_card.dat %sHTbinning%i_%i'%(outdir,outdir,binning[i],binning[i+1])
            os.system(cmd)
            if os.path.isfile('%scuts.f'%(outdir)):
                cmd='cp %scuts.f %sHTbinning%i_%i'%(outdir,outdir,binning[i],binning[i+1])
                os.system(cmd)

            
        for line in xrange(len(infile)):
            if 'ihtmin' in infile[line] :
                print infile[line]
                infile[line]='%.1f = ihtmin  !inclusive Ht for all partons (including b)\n'%(binning[i])
            if 'ihtmax' in infile[line]:
                print infile[line]
                infile[line]='%.1f = ihtmax  !inclusive Ht for all partons (including b)\n'%(binning[i+1])
        with open("%sHTbinning%i_%i/run_card.dat"%(outdir,binning[i],binning[i+1]), "w") as f1:
            f1.writelines(infile)            
#__________________________________________________________
if __name__=="__main__":
    Dir = os.getcwd()
    
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option ('-i','--inputcard', help='input madgraph run card',
                       dest='inputcard',
                       default='')

    parser.add_option ('-p', '--process',  help='process to bin',
                       dest='process',
                       default='')

    parser.add_option ('-b', '--binning',  help='binning file',
                       dest='binning',
                       default='')

    (options, args) = parser.parse_args()
    inputcard  = options.inputcard
    process    = options.process
    binning    = options.binning
    
    with open(binning) as binning_file:    
        data = json.load(binning_file)
    print data[process]
    
    writecards(data[process], inputcard)
