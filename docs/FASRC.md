# Continuing on FASRC

The GitHub project transfers the research state without sharing cluster credentials. You sign into FASRC using your existing access and clone the public repository there.

1. Choose lab storage for the repository, downloaded events and outputs. The first complete CMS acquisition is 310.24 GB; roughly 0.5-1 TB is a planning allowance for input plus working outputs, not a guaranteed final requirement. The complete ATLAS 2015-2016 files total 49.18 TB and should be approached through selective reading/skimming.
2. Clone the repository and run `python3 scripts/materialize.py`. This needs no network after cloning.
3. Review the report, `inventory/dataset_inventory.json`, and the HEPData gaps before deciding which events to acquire.
4. Test the four sample downloads using `python3 scripts/restore_samples.py --execute`, then run the restored collection's `verify_package.py`.
5. Use the restored `acquire_events.py` for the CMS records 30525 and 30558. It defaults to a dry run, accepts an explicit GB budget and verifies file checksums.

Use your lab's approved transfer arrangements for bulk downloads. Run substantial analysis under Slurm rather than on a shared login node. The proper account, partition, output path and software modules depend on your FASRC allocation; this repository does not assume them or submit any cluster jobs.

For Python exploration, create an environment and install `requirements-analysis.txt`. These are compatibility ranges rather than a frozen validated physics environment. The older CMS analyst code needs its documented CMSSW/Combine setup and unresolved external dependencies. Reading a ROOT file does not validate a complete statistical model.

Relevant official documentation:

- [FASRC running jobs](https://docs.rc.fas.harvard.edu/kb/running-jobs/)
- [FASRC cluster responsibilities](https://docs.rc.fas.harvard.edu/kb/responsibilities/)
- [FASRC SCP/SFTP transfers](https://docs.rc.fas.harvard.edu/kb/copying-data-to-and-from-cluster-using-scp/)
- [FASRC Globus transfers](https://docs.rc.fas.harvard.edu/kb/globus-file-transfer/)
- [CMS NanoAOD guide](https://opendata.cern.ch/docs/cms-getting-started-nanoaod)

SSH access for an assistant is not required to transfer this work. Remote execution would be a separate step requiring a supported connection and your institution's approved access method; it is not configured here.
