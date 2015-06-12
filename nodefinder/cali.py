#!/usr/bin/env python


"""Do calibration for Nekwik format trees.

[Usage]
    Fill in all the necessary informations in cali.ini, then run this in
    command line:

    python cali.py
"""

from __future__ import print_function, with_statement

import os
import re
import sys


__version__ = '0.1.2'

CONFIG_FILE = 'cali.ini'


USAGE_INFO = r"""
Usage:

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
"""

INI_FILE_TEMPLATE = r"""
#===================================================#
#    Tree File Name or Path (Only one)
#===================================================#

test.nwk

#==========================================================#
#    Calibration Information (One or multiple)
#==========================================================#

c, b, >0.05<0.07
a, e, >0.04<0.06
c, f, >0.3<0.5


#==============================================================================
#    Usage:
#==============================================================================
#
# Put these three files:
#
# 1. `cali.py` (The main script);
# 2. `cali.ini` (Config file for cali.py);
# 3. `tree_file.nwk` (The Newick tree you want to do calibration).
#
# in the same folder, then run this command in command line:
#
#     python cali.py
#
#
#
# ### `cali.ini` File Syntax:
#
#     # Lines start with '#' will be ignored.
#
#     # tree file name
#     tree_file_name.nwk
#
#     # calibrations
#     name_a, name_b, calibration_infomation_1
#     name_c, name_d, calibration_infomation_2
#     ..., ..., ...
#
#
#
# ### Tips:
#
# 0. You want to run this program in Windows cmd or Command Line to see
#    outcomes and **error messages**;
# 1. Tree file should be **Newick** format file (Multi lines are accepted);
# 2. If first line is like this: '72  1', it's OK;
# 3. Lines start with "#" will be ignored (Considered as comments);
# 4. Separate elements in each calibration line with '**,**';
# 5. Each calibration one line;
# 6. If calibration at specific node already exists, it will be replaced by
#    new one;
# 7. A new tree file will be generated. Please check your working dir.
#
#
#
# ### For Example:
#
# Say we have a tree file: "`test.nwk`":
#
#     ((a ,((b, c), (d, e))), (f, g));
#
# Run this command at command line:
#
#     python cali.py
#
# If no `cali.ini` file in current dir, after running the command, the program
# will generate this config file and gives you informations like this:
#
#     =====================================================
#     [Config FILE Generated]:
#         Please modify cali.ini and run this program again.
#     =====================================================
#
#     Usage:
#         ...
#
#     Example:
#         ...
#
#     Tips:
#         ...
#
# Then modify `cali.ini`:
#
#     # Comments will be ignored
#
#     # Newick tree file name
#
#     test.nwk
#
#     # Calibrations
#     # (calibration_info can be: >0.05<0.07, @0.144, >0.6, ...)
#     # species_name_a, species_name_b, calibration_info
#
#     # Add '>0.05<0.07' to the most recent common node of c and b
#     c, b, >0.05<0.07
#     a, e, >0.1<0.2
#     c, f, >0.3<0.5
#
# Run this command again at command line to do calibrations:
#
#     python cali.py
#
# The we will get a new tree with calibration informations:
#
#     ((((a, b), c)>0.05<0.07, (d, e))>0.1<0.2, (f, g))>0.3<0.5;
#
# And a file named "`test.cali.nwk`" will be genereated.
#
# PLEASE USE SOFTWARES LIKE TreeView TO CHECK THE OUTCOME!!
#
#             +---------- a
#             |
#             | >0.1<0.2
#         +---|       +-- b
#         |   |   +---| >0.05<0.07
#         |   |   |   +-- c
#         |   +---|
#         |       |   +-- d
#         |       +---|
#     ----|>0.3<0.5   +-- e
#         |
#         |           +-- f
#         +-----------|
#                     +-- g
#
# ### Informations and Warnings Given by This Program:
#
# 1. Tipical Outcome Information:
#
#         [2]:  a, e, >0.1<0.2
#         ----------------------------------------------------
#         [Name A]:   a
#         [Name B]:   e
#         [ Cali ]:   >0.1<0.2
#         [Insert]:   c)>0.05<0.07,(d,e))),(f,g));
#         [Insert]:                    ->||<-
#         ----------------------------------------------------
#
#         # Comments:
#
#         [2]: a, e, >0.1<0.2:
#             This tells us the program is dealing with second calibration
#             line now.
#
#         [Insert]:
#             This tells us which place to insert calibration in the Newick
#             tree.
#
# 2. If calibration already exists at the node you want to add calibration,
#    a WARNING will be given by the program:
#
#         [Calibration Exists]:           >0.1<0.2   [- Old]
#         [Calibration Replaced By]:      >0.15<0.2  [+ New]
#
# 3. If two lines in your `cali.ini` file try to add calibration at the same
#    node, a WARNING will be given by the program:
#
#         !!! [Warning]   Duplicate calibration:
#         [Exists]:   a, b, >0.1<0.2
#         [ Now  ]:   a, c, >0.2<0.3
#
#     And the last line of calibration will be the final calibration at this
#     node.
"""
CONFIRM_INFO = '\n\nPress Enter to exit...'

_insertion_list_point_dict = {}


class ConfigFileSyntaxError(SyntaxError):
    """Error class for config file"""
    pass


def clean_elements(orig_list):
    """Strip each element in list and return a new list.
    [Params]
        orig_list: Elements in original list is not clean, may have blanks or
                   newlines.
    [Return]
        clean_list: Elements in clean list is striped and clean.

    [Example]
        >>> clean_elements(['a ', '\tb\t', 'c\n'])
        ['a', 'b', 'c']
    """
    return [_.strip() for _ in orig_list]


def get_clean_tree_str(tree_str):
    """Remove all blanks and return a very clean tree string.
    >>> get_clean_tree_str(((a ,((b, c), (d, e))), (f, g));)
    '((a,((b,c),(d,e))),(f,g));'
    """
    return tree_str.replace(' ', '').replace('\n', '').replace('\t', '')


def find_right_paren(clean_tree_str, left_index_now):
    """Find the index of paired right parenthesis ')' of given '('."""
    stack = []
    paren_index_right = left_index_now
    stack.append('(')
    while len(stack) > 0:
        paren_index_right += 1
        if clean_tree_str[paren_index_right] == '(':
            stack.append('(')
        elif clean_tree_str[paren_index_right] == ')':
            stack.pop()
    return paren_index_right


def find_first_left_paren(clean_tree_str, one_name):
    """Find the index of first '(' on the left side of given name."""
    index_left = clean_tree_str.find(one_name)
    while clean_tree_str[index_left] != '(':
        index_left -= 1
    return index_left


def find_first_right_paren(clean_tree_str, one_name):
    """Find the index of first ')' on the right side of given name."""
    index_right = clean_tree_str.find(one_name)
    while clean_tree_str[index_right] != ')':
        index_right += 1
    return index_right


def left_side_left_paren(clean_tree_str, left_index_now):
    """Find first '(' on the left side of current '('."""
    stack = []
    stack.append(')')
    while len(stack) > 0:
        if left_index_now == 0:
            return left_index_now
        left_index_now -= 1
        if clean_tree_str[left_index_now] == ')':
            stack.append(')')
        elif clean_tree_str[left_index_now] == '(':
            if len(stack) == 1:
                return left_index_now
            stack.pop()
        else:
            continue
    return left_index_now


def get_insertion_list(clean_tree_str, name_to_find):
    """Get a list of insertition point index and return it."""
    insertion_list = []
    left_index_now = clean_tree_str.find(name_to_find) - 1
    if clean_tree_str[left_index_now] != '(' and\
            clean_tree_str[left_index_now] == ',':
        index_right_paren = find_first_right_paren(
            clean_tree_str, name_to_find)
        # insertion_list.append(index_right_paren+1)
        left_index_now = index_right_paren
    else:
        left_index_now = clean_tree_str.find(name_to_find) - 1
        insertion_list.append(
            find_right_paren(clean_tree_str, left_index_now)+1)
    # print(left_index_now)
    while left_index_now >= 0:
        if left_index_now == 0:
            # final_point = find_right_paren(clean_tree_str, left_index_now)
            # print('Final point: ', final_point)
            # insertion_list.append(final_point + 1)
            # print('[Final Insertion List]: ', name_to_find,
            #       '\n\t\t\t', insertion_list)
            return insertion_list
        left_index_now = left_side_left_paren(clean_tree_str, left_index_now)
        # print('new index: %d' % left_index_now)
        insertion_list.append(
            find_right_paren(clean_tree_str, left_index_now) + 1)
        # print('Insertion list now: ', insertion_list)
    return insertion_list


def single_calibration(tree_str, name_a, name_b, cali_info):
    """Do single calibration. If calibration exists, replace it."""
    clean_tree_str = get_clean_tree_str(tree_str)
    insertion_list_a = get_insertion_list(clean_tree_str, name_a)
    insertion_list_b = get_insertion_list(clean_tree_str, name_b)
    insertion_list_a, insertion_list_b = insertion_list_a[::-1],\
        insertion_list_b[::-1]
    shorter_list = insertion_list_a if len(insertion_list_a) <\
        len(insertion_list_b) else insertion_list_b
    longer_list = insertion_list_a if shorter_list == insertion_list_b else\
        insertion_list_b
    # print('[Shorter List]: ', shorter_list)
    # print('[Longer List]:  ', longer_list)
    for i, each_in_shorter_list in enumerate(shorter_list):
        if i == len(shorter_list) - 1:
            cali_point = each_in_shorter_list
        if shorter_list[i] != longer_list[i]:
            cali_point = shorter_list[i - 1]
            break
    # print('[Common]:         ', cali_point)
    print('[Insert]:  ', clean_tree_str[cali_point-20:cali_point+20])
    print('[Insert]:  ', '                 ->||<-                ')

    # Check if there are duplicate calibration
    current_info = '%s, %s, %s' % (name_a, name_b, cali_info)
    if cali_point not in _insertion_list_point_dict:
        _insertion_list_point_dict[cali_point] = current_info
    else:
        print('\n!!! [Warning]   Duplicate calibration:\n[Exists]:   %s\n'
              '[ Now  ]:   %s\n' % (_insertion_list_point_dict[cali_point],
                                    current_info))

    # No calibration before
    if clean_tree_str[cali_point] in [',', ';', ')']:
        left_part, right_part = clean_tree_str[:cali_point],\
            clean_tree_str[cali_point:]
        clean_str_with_cali = left_part + cali_info + right_part
    # There was calibration there
    # '>':  >0.05<0.07
    # '<':  <0.38
    # '@':  @0.56
    # '0':  0.5
    # '1':  1
    # "'":  '>0.05<0.07'
    # '"':  ">0.05<0.07"
    elif clean_tree_str[cali_point] in ['>', '<', '@', '0', '1', "'", '"']:
        # ((a,((b,c),(d,e)))>0.3<0.5,(f,g));
        # left_part = '((a,((b,c),(d,e)))'
        # right_part = '>0.3<0.5,(f,g));'
        # re will find '>0.3<0.5' part
        re_find_left_cali = re.compile('^[^,);]+')
        left_part, right_part = clean_tree_str[:cali_point],\
            clean_tree_str[cali_point:]
        left_cali = re_find_left_cali.findall(right_part)[0]
        print('[Calibration Exists]:          ', left_cali, '  [- Old]')
        print('[Calibration Replaced By]:     ', cali_info, '  [+ New]')
        # '>0.3<0.5,(f,g));'.lstrip('>0.3<0.5') will be ',(f,g));'
        final_right_part = right_part.lstrip(left_cali)
        clean_str_with_cali = left_part + cali_info + final_right_part
    else:
        raise ValueError('Unknown: ' + clean_tree_str[cali_point])
    return clean_str_with_cali


def multi_calibration(tree_str, cali_tuple_list):
    """Do calibration for multiple calibration requests."""
    for i, each_cali_tuple in enumerate(cali_tuple_list):
        name_a, name_b, cali_info = each_cali_tuple
        print('\n\n')
        print('[%d]:  %s' % (i+1, ', '.join(each_cali_tuple)))
        print('-' * 52)
        print('[Name A]:  ', name_a)
        print('[Name B]:  ', name_b)
        print('[ Cali ]:  ', cali_info)
        for name in [name_a, name_b]:
            if name not in tree_str:
                raise ConfigFileSyntaxError('Name not in tree file:  ', name)
        if cali_info[0] not in ['>', '<', '@', '#']:
            print('\n!!! [Warning]: Is this valid calibration?  %s\n' %
                  cali_info)
        tree_str = single_calibration(tree_str, name_a, name_b, cali_info)
        print('-' * 52)
    return tree_str.replace(',', ', ')


class ParseConfig(object):
    """Read and parse config file."""
    def __init__(self, ini_file_name):
        self.ini_file_name = ini_file_name
        self.cali_lines = []

    def read_ini(self):
        """Read ini config file and parse it."""
        if not os.path.isfile(self.ini_file_name):
            raise IOError('No ini file "%s" in current dir.' %
                          self.ini_file_name)
        with open(self.ini_file_name, 'r') as _:
            for line in _:
                line = line.strip()
                if line and not line.startswith('#') and\
                        not line.startswith('//'):
                    self.cali_lines.append(line)
        if len(self.cali_lines) <= 1:
            error_msg = ('There must be more than one calibration'
                         ' lines.\n%s' % USAGE_INFO)
            raise ConfigFileSyntaxError(error_msg)

    @property
    def tree_file_name(self):
        """Get tree file name from Config file."""
        _tree_file_name = self.cali_lines[0]
        if not os.path.isfile(_tree_file_name):
            error_msg = ('[ERROR] No such tree file in current dir: %s' %
                         _tree_file_name)
            raise IOError(error_msg)
        return _tree_file_name

    @property
    def cali_list(self):
        """Get calibration list from Config file."""
        tmp_cali_list = []
        for i, line in enumerate(self.cali_lines[1:]):
            elements = clean_elements(line.split(','))
            if len(elements) not in [2, 3]:
                error_msg = ('[Calibration lines]: name_a, name_b, cali_info\n'
                             '[Branch label lines]: name, branch_label(#)\n'
                             '[Clade label lines]:  name_a, name_b, '
                             'clade_ladel')
                raise ConfigFileSyntaxError('Invalid calibration line [%d]: %s'
                                            % (i + 1, line) +
                                            'Usage:\n\n%s' % error_msg)
            tmp_cali_list.append(elements)
        return tmp_cali_list


def get_tree_str(tree_file):
    """Read tree file, parse, and return tree string"""
    tmp_tree_str = ''
    tree_start_flag = False
    with open(tree_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('('):
                tree_start_flag = True
            if not tree_start_flag:
                continue
            if line.startswith('//') or line.startswith('#'):
                break
            else:
                tmp_tree_str += line
    return tmp_tree_str


def write_str_to_file(orig_tree_file_name, str_to_write):
    """Write string to a file"""
    re_extension = re.compile('[^.]+$')
    extension = re_extension.findall(orig_tree_file_name)[0]
    out_file_name = orig_tree_file_name.rstrip(extension) + 'cali.'\
        + extension
    with open(out_file_name, 'w') as f:
        f.write(str_to_write)
        print('\n[New Tree Written] >>>>> %s\n' % out_file_name)


def main():
    """Main fuction"""
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f_ini:
            f_ini.write(INI_FILE_TEMPLATE)
        with open('test.nwk', 'w') as f_nwk:
            f_nwk.write('((a ,((b, c), (d, e))), (f, g));')
        print('=' * 53)
        print('[Config FILE Generated]:\n    Please modify [cali.ini] '
              'and run this program again.')
        print('\n    A test tree file was also generated: [test.nwk]')
        print('    You can do practices with: [test.nwk] and [cali.ini]')
        print('        Run this at command line --> python cali.py')
        print('=' * 53)
        print(USAGE_INFO)
        sys.exit(1)
    c = ParseConfig(CONFIG_FILE)
    c.read_ini()
    tree_file_name, calibration_list = c.tree_file_name, c.cali_list

    tree_str = get_tree_str(tree_file_name)
    tree_with_cali = multi_calibration(tree_str, calibration_list)
    print('\n\n' + '=' * 52)
    try:
        write_str_to_file(tree_file_name, tree_with_cali)
    except IOError:
        print('[ERROR]:  Cannot write calibration tree to file.')
    finally:
        print('[Tree With Calibration]:\n\n', tree_with_cali)
        print('\n' + '=' * 52)


if __name__ == '__main__':
    main()
