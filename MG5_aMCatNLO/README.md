[]() MG5_aMCatNLO grid pack submissions scripts
================================================

**NOTE: These scripts have been adapted from [CMS submission scripts](https://github.com/cms-sw/genproductions).**
(Special thanks to J. Bendavid and P. Govoni).

-   [General instructions](#instructions)
-   [Local submission](#local)
-   [LSF Batch submission](#batch)

[]() General instructions
--------------------------

The process to be generated and the desired cuts and settings are defined in a set of cards:

-   ```[process_name]_proc_card.dat```, where one declares the process to be generated [MANDATORY]
-   ```[process_name]_run_card.dat```, where one defines particular options on how the generator will run and generate the process, as well as specific kinematic cut values [MANDATORY]
-   ```[process_name]_madspin_card.dat```, where one instructs MadSpin on how to decay specific particles (optional). 

There exist other two cards,

-   ```[process_name]_customizecards.dat```, where one would set the values of the parameters of the model, such as masses and couplings. In the general use case, this card needs not be modified by the users: the default card contains the agreed-upon values to be used for all processes.
-   ```[process_name]_extramodels.dat```: if non-SM lagrangians need to be used for the generations, they must be declared here and the related tarballs must be uploaded to the generator web repository. 

Here [process_name] is a string of your choice: it can be whatever string, but it should be the same string for all the cards.

Examples of cards:

-   [proc_card](./cards/examples/pp_w012j_5f/pp_w012j_5f_proc_card.dat) for a LO process.
-   [run_card](./cards/examples/pp_w012j_5f/pp_w012j_5f_run_card.dat) for a LO process.
-   [customize](./cards/examples/pp_hh_bbaa/pp_hh_bbaa_customizecards.dat) card.
-   [extra model](./cards/examples/pp_hh_bbaa/pp_hh_bbaa_extramodels.dat) card.


[]() Local submission
----------------------


For a relatively simple process (< 4 matched partons) the master job can be sent locally. Daughter jobs are sent to the cluster automatically.
This requires the user to stay logged in the same machine for the duration of the job.

On an lxplus machine, type do the following:

```
git clone https://github.com/selvaggi/GridPackProducer
cd GridPackProducer/MG5_aMCatNLO/
./gridpack_generation.sh [output_folder] [cards_folder] [queue]
```

e.g.

```
./gridpack_generation.sh pp_w012j_5f cards/examples/pp_w012j_5f 1nd
```

[]() LSF batch submission
-------------------------

For longer jobs (>4 matched partons) it is suggested to run the master on the cluster, on a long queue.

```
./submit_gridpack_generation.sh [memoryMb] [diskMb] [queue_master] [output_folder] [cards_folder] [queue_daughter]
```

e.g

```
./submit_gridpack_generation.sh 15000 15000 2nw pp_w01234j_5f cards/examples/pp_w01234j_5f 8nh
```

