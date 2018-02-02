# python createScan.py --p ../cards/production/pp_Zprime_mumu_5f  -l list.txt

import json
import os, glob
import os.path


#_________________________________________________________________________________
def copy_card(incard, outcard):
    if not os.path.exists(outcard) and os.path.exists(incard):
        cmd = 'cp {} {}'.format(incard, outcard)
        os.system(cmd)

#__________________________________________________________________________________
def write_cards(procdir, procDict, plist):
    
    os.system('rm {}'.format(plist))

    for procstr, custom_str in procDict.iteritems():
        new_procdir = procdir + '/' + os.path.basename(procdir) + '_' + procstr 
      
        if not os.path.exists(os.path.dirname(plist)):
            os.makedirs(os.path.dirname(plist))

        with open(plist, "a") as lfile:
            lfile.write('cards/production/'+ os.path.basename(procdir) + '/' + os.path.basename(procdir) + '_' + procstr + '\n')

        if not os.path.exists(new_procdir):
            os.makedirs(new_procdir)
            old_cuts_file = procdir + '/cuts.f'           
            old_scut_file = procdir + '/setcuts.f'           
            old_proc_file = procdir + '/proc_card.dat'           
            old_runc_file = procdir + '/run_card.dat'           
            old_cust_file = procdir + '/customizecards.dat'           
            old_extr_file = procdir + '/extramodels.dat'           
            new_cuts_file = new_procdir + '/cuts.f'
            new_scut_file = new_procdir + '/setcuts.f'           
            new_proc_file = new_procdir + '/proc_card.dat'
            new_runc_file = new_procdir + '/run_card.dat'
            new_cust_file = new_procdir + '/customizecards.dat'
            new_extr_file = new_procdir + '/extramodels.dat'           
          
            copy_card(old_cuts_file, new_cuts_file)
            copy_card(old_scut_file, new_scut_file)
            copy_card(old_proc_file, new_proc_file)
            copy_card(old_runc_file, new_runc_file)
            copy_card(old_cust_file, new_cust_file)
            copy_card(old_extr_file, new_extr_file)

            # until now was simply copying main process, now write specific subprocess stuff
            if os.path.exists(new_cust_file):
               with open(new_cust_file, "a") as myfile:
                   myfile.write(custom_str)

#___________________________________________________________________________________________
def ZpParamList():

   #ref point
   mzp_ref = 2000.
   gmu_ref = 0.4
   gbs_ref = 0.9200000e-02

   custom_dict = dict()

   for i in xrange(1, 10):
       mzp = mzp_ref*float(i)
       gmu = gmu_ref*float(i)
       gbs = gbs_ref*float(i)

       custom_str =''       
       custom_str += 'set param_card mzp {}\n'.format(mzp)
       custom_str += 'set param_card gmu {}\n'.format(gmu)
       custom_str += 'set param_card gbs {}\n'.format(gbs)
       custom_str += 'set param_card Wzp Auto\n'
       
       proc_str = 'Mzp_{:.0f}TeV'.format(mzp/1000.)
       print proc_str, custom_str
       custom_dict[proc_str] = custom_str

   return custom_dict 


#__________________________________________________________
if __name__=="__main__":
    Dir = os.getcwd()
    
    
    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option ('-p', '--procdir',  help='process directory',
                       dest='procdir',
                       default='')

    parser.add_option ('-l', '--list',  help='process output list file',
                       dest='list',
                       default='')

   
    (options, args) = parser.parse_args()
    procdir = options.procdir
    plist   = options.list
    
    procDict = ZpParamList()
    write_cards(procdir, procDict, plist)

