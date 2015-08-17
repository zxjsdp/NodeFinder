NodeFinder
==========

[![Build Status](https://travis-ci.org/zxjsdp/NodeFinder.svg?branch=master)](https://travis-ci.org/zxjsdp/NodeFinder)
[![Coverage Status](https://coveralls.io/repos/zxjsdp/NodeFinder/badge.svg)](https://coveralls.io/r/zxjsdp/NodeFinder)

Tools for node related operations in phylogenetic analyses

GUI Version
-----------

If you are not familiar with console or you prefer Graphical User Interface,
please refer to [NodeFinderGUI](https://github.com/zxjsdp/NodeFinderGUI).

It's an GUI implementation of NodeFinder with Python tkinter.

cali.py
-------

Do multiple calibrations at the most recent common ancestor node.

### Requirements

For Linux, Windows, and Mac OS X users:

You need Python 2.6 or Python 3.x to run this script.

    python cali.py

Otherwise, For Windows users:

1. If you do not have Python environment in your computer;
2. Or if you only have Python version lower than Python 2.6;

please go to this web page and download the latest version of
**Single-File Stand-alone Python** 2.7 for Windows:

**Go to Webpage**: <http://www.orbitals.com/programs/pyexe.html>

**Directly download py.exe**: <http://www.orbitals.com/programs/py.exe>

Then run this at command line:

    py.exe cali.py

### Usage

Put these three files:

1. `cali.py` (The main script);
2. `cali.ini` (Config file for cali.py);
3. `tree_file.nwk` (The Newick tree you want to do calibration).

in the same folder, then run this command in command line:

    python cali.py



### Config File Syntax (`cali.ini`):

    // Lines start with # or // will be ignored.
    [Tree File Name]

        tree_file_name.nwk

    [Calibration or Label Infos, One or Multiple]

        name_a, name_b, calibration_infomation_1
        name_c, name_d, calibration_infomation_2
        name_a, name_b, clade_label_information
        name, branch_label_information
        ..., ..., ...

#### Example One (Do calibrations):

    [Tree File Name]

        test.nwk

    [Calibration or Label Infos, One or Multiple]

        a, b, >0.05<0.07
        c, d, >0.08<0.09

#### Example Two (Add branch labels or clade labels):

    [Tree File Name]

        test.nwk

    [Calibration or Label Infos, One or Multiple]

        d, e, $1
        a, #1

### Tips:

0. You want to run this program in Windows cmd or Command Line to see
   outcomes and **error messages**;
1. Tree file should be **Newick** format file (Multi lines are accepted);
2. If first line is like this: `72  1`, it's OK;
3. Lines start with "#", "\\" will be ignored
   (Considered as comments);
4. Separate elements in each line with `,`;
5. Each calibration or branch label or clade label one line;
6. If calibration or branch label or clade label at specific node already
   exists, it will be replaced by new one;
7. A new tree file will be generated. Please check your working dir.



### For Example:

Say we have a tree file: "`test.nwk`":

    ((a ,((b, c), (d, e))), (f, g));

Run this command at command line:

    python cali.py

If no `cali.ini` file in current dir, after running the command, the program
will generate this config file and gives you informations like this:

    =====================================================
    [Config FILE Generated]:
        Please modify [cali.ini] and run this program again.

        A test tree file was also generated: [test.nwk]
        You can do practices with: [test.nwk] and [cali.ini]
            Run this at command line --> python cali.py
    =====================================================

    Usage:

    [cali.ini Syntax]:
        ...

    [Example]:
        ...

    [Tips]:
        ...

Modify `cali.ini`:

    // Comments will be ignored
    // Newick tree file name

    [Tree File Name]

        test.nwk

    // (Info can be: >0.05<0.07, @0.144, >0.6, #1, $1, "#1", ...)
    // name_a, name_b, info
    // Add '>0.05<0.07' to the most recent common node of c and b

    [Calibration or Label Infos, One or Multiple]

    // This is just for test, so we add calibrations and branch labels
       and clade labels at the same time.


         c, b, >0.05<0.07
         a, e, >0.04<0.06
         c, f, >0.3<0.5
         d, e, $1
         a, #1

    // End

Run this command again at command line to do calibrations:

    python cali.py

Then we will get a new tree with calibration informations:

    ((((a #1 , b), c)>0.05<0.07, (d, e)$1)>0.1<0.2, (f, g))>0.3<0.5;

And a file named "`test.cali.nwk`" will be genereated.

PLEASE USE SOFTWARES LIKE TreeView TO CHECK THE OUTCOME!!

            +---------- a #1
            |
            | >0.1<0.2
        +---|       +-- b
        |   |   +---| >0.05<0.07
        |   |   |   +-- c
        |   +---|
        |       |   +-- d
        |       +---| $1
    ----|>0.3<0.5   +-- e
        |
        |           +-- f
        +-----------|
                    +-- g

### INFORMATIONs and WARNINGs after Running:

1. Tipical Outcome Information:

        [2]:  a, e, >0.1<0.2
        ----------------------------------------------------
        [Name A]:   a
        [Name B]:   e
        [ Cali ]:   >0.1<0.2
        [Insert]:   c)>0.05<0.07,(d,e))),(f,g));
        [Insert]:                    ->||<-
        [Insert]:                  Insert Here
        ----------------------------------------------------

        # Comments:

        [2]: a, e, >0.1<0.2:
            This tells us the program is dealing with second calibration line now.

        [Insert]:
            This tells us which place to insert calibration in the Newick tree.

2. If calibration already exists at the node you want to add calibration,
   a WARNING will be given by the program: 

        [Calibration Exists]:           >0.1<0.2   [- Old]
        [Calibration Replaced By]:      >0.15<0.2  [+ New]

3. If two lines in your `cali.ini` file try to add calibration at the same
   node, a WARNING will be given by the program:

        !!! [Warning]   Duplicate calibration:
        [Exists]:   a, b, >0.1<0.2
        [ Now  ]:   a, c, >0.2<0.3

    And the last line of calibration will be the final calibration at this
    node.
