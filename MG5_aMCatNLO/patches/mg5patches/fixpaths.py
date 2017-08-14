incard = './SubProcesses/job_status.pkl'

with open(incard) as f:
    infile = f.readlines()
    for line in xrange(len(infile)):
        if 'SubProcesses' in infile[line] :
            fpath, fvalue = infile[line].split("SubProcesses",1)
            infile[line]="S'./SubProcesses%s"%(fvalue)
    
with open(incard, "w") as f1:
    f1.writelines(infile)
