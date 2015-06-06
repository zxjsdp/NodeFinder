NodeFinder: Tools for node related operations in phylogenetic analyses
======================================================================

cali.py
-------

### Usage

Fill in all the necessary informations in cali.ini, then run this in
command line:

    $ python cali.py

[cali.ini Syntax]:

    # Lines start with # or // will be ignored.

    # tree file name
    tree_file_name.nwk

    # calibrations
    name_a, name_b, calibration_infomation_1
    name_c, name_d, calibration_infomation_2
    ..., ..., ...

[Example]:

    test.nwk

    a, b, >0.05<0.07
    c, d, >0.08<0.09

[Tips]:

    0. You want to run this program in Windows cmd or Command Line to see
       outcomes and error messages;
    1. Tree file should be nwk format file (Multi lines are accepted);
    2. If first line is like this: '72  1', it's OK;
    3. Lines start with "#" or '//' will be ignored (Considered as comments);
    4. Separate elements in each calibration line with ',';
    5. Newline (\n) indicate a new calibration;
    6. If calibration at specific node already exists, it will be replaced by
       new one;
    7. A new tree file will be generated. Please check your working dir.
