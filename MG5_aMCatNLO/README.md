[]() MG5_aMCatNLO grid pack submissions scripts
================================================

**For a relatively simple process (LO+0/1/2 matched partons) the master job can be sent locally. Daughter jobs are sent to the cluster automatically.
This requires the user to stay logged in the same machine for the duration of the job**.

On an lxplus machine, type do the following:

```
git clone https://github.com/selvaggi/GridPackProducer
cd GridPackProducer/MG5_aMCatNLO/
./gridpack_generation.sh <name of process card> <folder containing cards relative to current location> <queue>
```

e.g.

```
./gridpack_generation.sh pp_w012j_5f cards/examples/pp_w012j_5f 1nd
```

**For longer jobs (>3 matched partons) it is suggested to run the master on the cluster, on a long queue.**

```
./submit_gridpack_generation.sh <memoryInMBytes> <diskInMBytes> <queueForMasterJob> <name of process card> <folder containing cards relative to current location> <queueForDaughterJobs>
```

e.g

```
./submit_gridpack_generation.sh 15000 15000 2nw pp_w01234j_5f cards/examples/pp_w01234j_5f 8nh
```

