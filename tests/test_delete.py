import os

import pytest

from faim_robocopy.utils import delete_existing


def test_delete_duplicates(tmpdir):
    '''test deleting of copied files.

    '''
    # setup
    source = tmpdir.mkdir('source_dir')
    dest1 = tmpdir.mkdir('dest_dir_1')
    dest2 = tmpdir.mkdir('some_other_dir').mkdir('/dest_dir_2')

    # Add some empty folders
    empties = [source.mkdir('non').mkdir('sense'), source.mkdir('is_empty')]
    empties_not_for_deletion = [
        dest1.mkdir('nonsense'),
    ]

    files_in = {
        source: ['a.txt', 'b.ini', 'some.txt', 'thing.txt'],
        dest1: ['a.txt', 'b.ini', 'some.txt', 'another.txt'],
        dest2: ['b.ini', 'thing.txt']
    }

    for folder in files_in.keys():
        for filename in files_in[folder]:
            filehandle = folder.join(filename)
            filehandle.write(filename)

    delete_existing(str(source), [str(dest1), str(dest2)])

    # check that all files exists.
    for folder in [dest1, dest2]:
        for filename in files_in[folder]:
            assert os.path.exists(os.path.join(str(folder), filename))

    for filename in files_in[source]:
        if filename == 'b.ini':  # this should have been deleted!
            continue
        assert os.path.exists(os.path.join(str(source), filename))

    # check that copied file is removed from source.
    assert not os.path.exists(os.path.join(str(source), 'b.ini'))

    # check if empty folders are treated correctly.
    for empty_dir in empties:
        assert not os.path.exists(str(empty_dir))

    for empty_dir in empties_not_for_deletion:
        assert os.path.exists(str(empty_dir))