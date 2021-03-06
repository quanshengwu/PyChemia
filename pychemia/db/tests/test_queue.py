#!/usr/bin/env python

import os
import pychemia
import tempfile
import shutil
from pychemia.utils.computing import hashfile
from pychemia import HAS_PYMONGO, HAS_GRIDFS


def notest_queue():
    """
    Testing PyChemiaQueue               :
    """
    if not HAS_PYMONGO or not HAS_GRIDFS:
        print('PyChemiaQueue was disabled')
        return

    print("Testing PyChemiaQueue")

    source = 'pychemia/test/data/vasp_01'
    destination = tempfile.mkdtemp()
    print('Destination: %s' % destination)

    st = pychemia.code.vasp.read_poscar(source + os.sep + 'POSCAR')
    print('Structure: \n%s' % st)

    vi = pychemia.code.vasp.read_incar(source + os.sep + 'INCAR')
    print('VASP Input: \n%s' % vi)

    pq = pychemia.db.PyChemiaQueue()

    files = [source + os.sep + 'KPOINTS']
    entry_id = pq.new_entry(structure=st, variables=vi, code='vasp', files=files)

    nfiles = pq.db.fs.files.count()
    print('Number of files: ', nfiles)

    pychemia.code.vasp.write_from_queue(pq, entry_id, destination)

    for i in os.listdir(source):
        assert hashfile(source + os.sep + i) == hashfile(destination + os.sep + i)

    print('Files in source and destination are identical')

    print('Adding the same entry again and testing that the number of files is unchanged')
    entry_id = pq.new_entry(structure=st, variables=vi, code='vasp', files=files)

    assert nfiles == pq.db.fs.files.count()
    print('The number of files remains the same ', nfiles)

    shutil.rmtree(destination)


if __name__ == '__main__':
    test_queue()
