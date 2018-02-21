# python createScan.py --p ../cards/production/pp_Zprime_mumu_5f  -l list.txt

import json
import os, glob
import os.path
import collections

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

   custom_dict = collections.OrderedDict()

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

#___________________________________________________________________________________________
def LQParamList():

   #ref point
   mLQ_ref = 2000.
   g22_ref = 0.0268
   g32_ref = 4*g22_ref

   custom_dict = collections.OrderedDict()

   for i in xrange(1, 21):
       mLQ = mLQ_ref*float(i)
       g22 = g22_ref*float(i)
       g32 = g32_ref*float(i)

       custom_str =''
       custom_str += 'set param_card mass 9000005 {}\n'.format(mLQ)
       custom_str += 'set param_card mass 9000006 {}\n'.format(mLQ)
       custom_str += 'set param_card mass 9000007 {}\n'.format(mLQ)
       custom_str += 'set param_card yLL1x1 0.0\n'
       custom_str += 'set param_card yLL1x2 0.0\n'
       custom_str += 'set param_card yLL1x3 0.0\n'
       custom_str += 'set param_card yLL2x1 0.0\n'
       custom_str += 'set param_card yLL2x2 {}\n'.format(g22)
       custom_str += 'set param_card yLL2x3 0.0\n'
       custom_str += 'set param_card yLL3x1 0.0\n'
       custom_str += 'set param_card yLL3x2 {}\n'.format(g32)
       custom_str += 'set param_card yLL3x3 0.0\n'
       #custom_str += 'set param_card decay 9000005 Auto\n'
       #custom_str += 'set param_card decay 9000006 Auto\n'
       #custom_str += 'set param_card decay 9000007 Auto\n'

       proc_str = 'MLQ_{:.0f}TeV'.format(mLQ/1000.)
       print proc_str, custom_str
       custom_dict[proc_str] = custom_str

   return custom_dict


#___________________________________________________________________________________________
def StopParamList():

   #ref point
   mStop_ref = 1000.

   custom_dict = collections.OrderedDict()

   for i in xrange(1, 12):
       mStop = mStop_ref*float(i)

       custom_str =''
       custom_str += 'set param_card mass 1000001 1000000.0\n'
       custom_str += 'set param_card mass 1000002 1000000.0\n'
       custom_str += 'set param_card mass 1000003 1000000.0\n'
       custom_str += 'set param_card mass 1000004 1000000.0\n'
       custom_str += 'set param_card mass 1000005 1000000.0\n'
       custom_str += 'set param_card mass 1000006 {}\n'.format(mStop)
       custom_str += 'set param_card mass 2000001 1000000.0\n'
       custom_str += 'set param_card mass 2000002 1000000.0\n'
       custom_str += 'set param_card mass 2000003 1000000.0\n'
       custom_str += 'set param_card mass 2000004 1000000.0\n'
       custom_str += 'set param_card mass 2000005 1000000.0\n'
       custom_str += 'set param_card mass 2000006 1000000.0\n'
       custom_str += 'set param_card mass 1000021 1000000.0\n'
       custom_str += 'set param_card mass 1000022 1000000.0\n'
       custom_str += 'set param_card mass 1000023 1000000.0\n'
       custom_str += 'set param_card mass 1000024 1000000.0\n'
       custom_str += 'set param_card mass 1000025 1000000.0\n'
       custom_str += 'set param_card mass 1000035 1000000.0\n'
       custom_str += 'set param_card mass 1000037 1000000.0\n'
       custom_str += 'set param_card mass 1000039 1000000.0\n'
       custom_str += 'set param_card mass 1000011 1000000.0\n'
       custom_str += 'set param_card mass 1000012 1000000.0\n'
       custom_str += 'set param_card mass 1000013 1000000.0\n'
       custom_str += 'set param_card mass 1000014 1000000.0\n'
       custom_str += 'set param_card mass 1000015 1000000.0\n'
       custom_str += 'set param_card mass 1000016 1000000.0\n'
       custom_str += 'set param_card mass 2000011 1000000.0\n'
       custom_str += 'set param_card mass 2000013 1000000.0\n'
       custom_str += 'set param_card mass 2000015 1000000.0\n'

       proc_str = 'mStop_{:.0f}TeV'.format(mStop/1000.)
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
    
    #procDict = ZpParamList()
    #procDict = LQParamList()
    procDict = StopParamList()
    write_cards(procdir, procDict, plist)

