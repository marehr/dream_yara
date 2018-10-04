#!/usr/bin/env python2
"""Execute the tests for DREAM-Yara.

The golden test outputs are generated by the script generate_outputs.sh.

You have to give the root paths to the source and the binaries as arguments to
the program.  These are the paths to the directory that contains the 'projects'
directory.

Usage:  run_tests.py SOURCE_ROOT_PATH BINARY_ROOT_PATH
"""
import logging
import os.path
import sys
import glob
import os


# Automagically add util/py_lib to PYTHONPATH environment variable.
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',
                                    'include', 'seqan', 'util', 'py_lib'))
sys.path.insert(0, path)


import seqan.app_tests as app_tests

log_transforms = [
	app_tests.RegexpReplaceTransform("[0-9\.\-e]+ sec", "0.0 sec"),
	app_tests.RegexpReplaceTransform("Free [0-9]+ of [0-9]+ MB", "Free 0 of 0 MB")
]

sam_transforms = [
	app_tests.RegexpReplaceTransform("@PG.*", "@PG")
]

def main(source_base, binary_base):
    """Main entry point of the script."""

    # gold standard binary files created on little endian
    if sys.byteorder != 'little':
        print ('Skipping tests for DREAM-Yara on big endian')
        print ('=====================================')
        return 0

    print ('Executing test for DREAM-Yara')
    print ('====================================')

    ph = app_tests.TestPathHelper(
        source_base, binary_base,
        'tests')  # tests dir

    # ============================================================
    # Auto-detect the binary path.
    # ============================================================

    path_to_dream_indexer = app_tests.autolocateBinary(
      binary_base, 'bin', 'dream_yara_indexer')

    path_to_ibf_filter = app_tests.autolocateBinary(
      binary_base, 'bin', 'dream_yara_build_filter')

    path_to_dream_mapper = app_tests.autolocateBinary(
      binary_base, 'bin', 'dream_yara_mapper')

    # ============================================================
    # Built TestConf list.
    # ============================================================

    # Build list with TestConf objects, analoguely to how the output
    # was generated in generate_outputs.sh.
    conf_list = []

    # ============================================================
    # Run Distributed indexer Tests
    # ============================================================

    for organism in ['64-viral']:
        # ============================================================
        # Split the genomes in to 64 bins.
        # ============================================================
        tempFastaDir = ph.outFile('%s-binned-genomes/' % organism)
        if not os.path.exists(tempFastaDir):
            os.makedirs(tempFastaDir)
        binFastaLen = 101 # each fasta entry is 100 lines long (101 including the header)
        inputFasta = open(ph.inFile('input/%s-genomes.fa' % organism), 'r').read().split('\n')
        for b in range(64):
            # First, get the slice
            binFasta = inputFasta[b*binFastaLen:(b+1)*binFastaLen]
            # Now open one file per bin and dump the part
            outputFasta = open(tempFastaDir + '/' + str(b) + '.fa', 'w')
            outputFasta.write('\n'.join(binFasta))
            outputFasta.close()

        # Get file extensions for the fm index files
        exts = [os.path.basename(fname).split('.', 1)[-1]
                for fname in glob.glob(ph.inFile('gold/%s-genomes.*' % organism))]

        outFileDir = ph.outFile('input/%s-binned-indices/' % organism)
        InfileNames = [tempFastaDir + str(b) + '.fa' for b in range(64)]
        fileNames = [str(b)+'.'+e for b in range(64) for e in exts]
        if not os.path.exists(outFileDir):
            os.makedirs(outFileDir)

        conf = app_tests.TestConf(
            program=path_to_dream_indexer,
            args=['-o', outFileDir] + InfileNames,
            to_diff=[(ph.inFile('gold/%s-binned-indices/%s' % (organism, fileName)),
                     ph.outFile(outFileDir+ fileName), 'md5') for fileName in fileNames])
        conf_list.append(conf)


    # ============================================================
    # Run DREAM-yara IBF Filter Tests compute
    # ============================================================

    ibf_args = ['-b', '64' ,'-t', '4' ,'-k', '19' ,'-nh', ' 2' ,'-bs', '1']
    for organism in ['64-viral']:
        conf = app_tests.TestConf(
            program=path_to_ibf_filter,
            args=[ph.outFile('%s-binned-genomes/' % organism),
                  '-o', ph.outFile('%s-binned-genomes.filter' % organism)] + ibf_args)
        conf_list.append(conf)


    # ============================================================
    # Run Single-End DREAM-Yara Tests
    # ============================================================

    dis_mapper_args = [
            ['-e', '3', '--threads', '1'],
            ['-e', '3', '--threads', '1', '-sm', 'record', '-s', '10'],
            ['-e', '3', '--threads', '1', '-sm', 'tag', '-s', '10']
            ]
    dis_mapper_suffix = ['t1', 'rec.t1', 'tag.t1']


    for organism in ['64-viral']:
        for i in range(0, len(dis_mapper_args)):

            basic = app_tests.TestConf(
                program=path_to_dream_mapper,
                args=[ph.inFile('gold/%s-binned-indices/' % organism),
                      ph.inFile('input/%s-reads.fa' % organism),
                      '-fi', ph.outFile('%s-binned-genomes.filter' % organism),
                      '-o', ph.outFile('%s-reads.%s.sam' % (organism, dis_mapper_suffix[i]))] +
                      dis_mapper_args[i],
                to_diff=[(ph.inFile('gold/%s-reads.%s.sam' % (organism, dis_mapper_suffix[i])),
                          ph.outFile('%s-reads.%s.sam' % (organism, dis_mapper_suffix[i])),
                          sam_transforms)])
            conf_list.append(basic)


    # ============================================================
    # Execute the tests
    # ============================================================

    failures = 0
    for conf in conf_list:
        res = app_tests.runTest(conf)
        # Output to the user.
        print (' '.join([conf.program] + conf.args))
        if res:
             print ('OK')
        else:
            failures += 1
            print ('FAILED')

    # Cleanup.
    ph.deleteTempDir()

    print ('==============================')
    print ('     total tests: %d' % len(conf_list))
    print ('    failed tests: %d' % failures)
    print ('successful tests: %d' % (len(conf_list) - failures))
    print ('==============================')
    # Compute and return return code.
    return failures != 0

if __name__ == '__main__':
    sys.exit(app_tests.main(main))
