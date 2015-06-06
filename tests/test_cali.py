
from __future__ import print_function, with_statement

import os
import pytest
from nodefinder.cali import *

# test_dir, _, test_file = os.path.abspath(__file__).rpartition('\\')
# TESTS_DATA_DIR = os.path.join(test_dir, 'data')

# Index of each position
#                        111111111122222222223
#              0123456789012345678901234567890
test_tree_1 = '((a ,((b, c), (d, e))), (f, g));'

# Index of each position
#                             1111111111222222
#                   01234567890123456789012345
clean_tree_str_1 = '((a,((b,c),(d,e))),(f,g));'

test_tree_2 = ('(Nostoc_azollae_0708,(((((AnaXP35,(AnaJAHN,(Ana1446,'
               'Anabaena_cylindrica_PCC_7122))),(Nos8941,(((Tri10178,'
               'Tri10269),((Anabaena_sp._PCC_7108,(A.NMC-1,(Tri2001,AnaMs2)))'
               ',(Ana001,AnaKVJ17))),(((Nostoc_punctiforme_PCC_73102,'
               '((((Fis7414,(Calothrix_PCC_6303,Calothrix_PCC_7103)),'
               '((((Microcoleus_PCC_7113,'
               'Coleofasciculus_chthonoplastes_PCC_7420),'
               '(Chroococcidiopsis_thermalis_PCC_7203,Gloeocapsa_PCC_7428)),'
               '((Chamaesiphon_PCC_6605,Crinalium_epipsammum_PCC_9333),'
               '(Dactylococcopsis_salina_PCC_8305,(Cyanothece_PCC_7424,'
               '((Cyanothece_PCC_8801,Cyanothece_PCC_8802),'
               '(Cyanobacterium_aponinum_PCC_10605,Synechocystis_PCC_6803))))'
               ')),((((((Prochlorococcus_marinus_MIT_9313,Synechococcus_sp._W'
               'H_8109),(Prochlorococcus_marinus_MIT_9301,Prochlorococcus_mari'
               'nus_MIT_9211)),Synechococcus_elongatus_PCC_6301),(Gloeobacter_'
               'violaceus_PCC_7421,((Ecoli_K12_DH10B,(Chlamydia_trachomatis_4'
               '34,Spirochaeta_thermophila_DSM_6192)),Met2661))),(Acaryochlori'
               's_marina_MBIC11017,(Thermosynechococcus_elongatus_BP-1,Cyanoth'
               'ece_PCC_7425))),(Synechococcus_PCC_7502,Trichodesmium_erythrae'
               'um_IMS101)))),(Calothrix_PCC_7507,Cylindrospermum_stagnale_PCC'
               '_7417)),(NosDe1,(Nostoc_PCC_7107,(Nostoc_PCC_7524,(Nostoc_PCC_'
               '7120,(((178,177),(175,174)),Anabaena_variabilis_ATCC_29413))))'
               '))),((Nod7804,Glo14),Cal4356)),(Ana1tu,(AnaBIR2,(((Ana9705,((1'
               '255,1250),Aph2012)),Aph-flos),(Ana299,Anabaena_90)))))))),Ana0'
               '8-05),Ana1616),Ana133),Ana1984);')
clean_tree_str_1 = test_tree_1.replace(' ', '').replace('\n', '')\
    .replace('\t', '')


def test_clean_elements():
    new_list = clean_elements(['a ', '\tb\t', 'c\n'])
    assert new_list == ['a', 'b', 'c']


def test_get_clean_tree_str():
    clean_tree_str = get_clean_tree_str(test_tree_1)
    assert clean_tree_str == '((a,((b,c),(d,e))),(f,g));'


def test_find_right_paren():
    index_1 = (find_right_paren(test_tree_1, 0))
    index_2 = (find_right_paren(test_tree_1, 1))
    index_3 = (find_right_paren(test_tree_1, 5))
    index_4 = (find_right_paren(test_tree_1, 6))
    index_5 = (find_right_paren(test_tree_1, 14))
    index_6 = (find_right_paren(test_tree_1, 24))
    assert index_1 == 30
    assert index_2 == 21
    assert index_3 == 20
    assert index_4 == 11
    assert index_5 == 19
    assert index_6 == 29


def test_left_side_left_paren():
    index_1 = left_side_left_paren(test_tree_1, 0)
    index_2 = left_side_left_paren(test_tree_1, 1)
    index_3 = left_side_left_paren(test_tree_1, 5)
    index_4 = left_side_left_paren(test_tree_1, 6)
    index_5 = left_side_left_paren(test_tree_1, 14)
    index_6 = left_side_left_paren(test_tree_1, 24)
    assert index_1 == 0
    assert index_2 == 0
    assert index_3 == 1
    assert index_4 == 5
    assert index_5 == 5
    assert index_6 == 0


@pytest.fixture(params=[
    "Nostoc_azollae_0708", "AnaXP35", "AnaJAHN", "Ana1446",
    "Anabaena_cylindrica_PCC_7122",
    "Nos8941", "Tri10178", "Tri10269", "Anabaena_sp._PCC_7108",
    "A.NMC-1", "Tri2001", "AnaMs2", "Ana001", "AnaKVJ17",
    "Nostoc_punctiforme_PCC_73102",
    "Fis7414", "Calothrix_PCC_6303", "Calothrix_PCC_7103",
    "Microcoleus_PCC_7113",
    "Coleofasciculus_chthonoplastes_PCC_7420",
    "Chroococcidiopsis_thermalis_PCC_7203",
    "Gloeocapsa_PCC_7428", "Chamaesiphon_PCC_6605",
    "Crinalium_epipsammum_PCC_9333",
    "Dactylococcopsis_salina_PCC_8305", "Cyanothece_PCC_7424",
    "Cyanothece_PCC_8801",
    "Cyanothece_PCC_8802", "Cyanobacterium_aponinum_PCC_10605",
    "Synechocystis_PCC_6803",
    "Prochlorococcus_marinus_MIT_9313", "Synechococcus_sp._WH_8109",
    "Prochlorococcus_marinus_MIT_9301", "Prochlorococcus_marinus_MIT_9211",
    "Synechococcus_elongatus_PCC_6301", "Gloeobacter_violaceus_PCC_7421",
    "Ecoli_K12_DH10B", "Chlamydia_trachomatis_434",
    "Spirochaeta_thermophila_DSM_6192",
    "Met2661", "Acaryochloris_marina_MBIC11017",
    "Thermosynechococcus_elongatus_BP-1",
    "Cyanothece_PCC_7425", "Synechococcus_PCC_7502",
    "Trichodesmium_erythraeum_IMS101",
    "Calothrix_PCC_7507", "Cylindrospermum_stagnale_PCC_7417", "NosDe1",
    "Nostoc_PCC_7107", "Nostoc_PCC_7524", "Nostoc_PCC_7120", "178",
    "177", "175", "174", "Anabaena_variabilis_ATCC_29413", "Nod7804",
    "Glo14", "Cal4356", "Ana1tu", "AnaBIR2", "Ana9705", "1255",
    "1250", "Aph2012", "Aph-flos", "Ana299", "Anabaena_90",
    "Ana08-05", "Ana1616", "Ana133", "Ana1984"
    ])
def tree_cyano_names(request):
    return request.param


def test_get_insertion_list(tree_cyano_names):
    list_1 = get_insertion_list(test_tree_1, 'a')
    list_2 = get_insertion_list(test_tree_1, 'b')
    list_3 = get_insertion_list(test_tree_1, 'd')
    list_4 = get_insertion_list(test_tree_1, 'f')
    assert list_1 == [22, 31]
    assert list_2 == [12, 21, 22, 31]
    assert list_3 == [20, 21, 22, 31]
    assert list_4 == [30, 31]
    assert len(get_insertion_list(test_tree_2, tree_cyano_names)) >= 1


def test_single_calibration():
    out_1 = single_calibration(test_tree_1, 'a', 'b', '>0.3<0.5')
    print('OUT 1: ', out_1)
    assert out_1 == '((a,((b,c),(d,e)))>0.3<0.5,(f,g));'
    out_2 = single_calibration('((a,((b,c),(d,e)))>0.3<0.5,(f,g));', 'a', 'b',
                               '>0.7<0.9')
    print('OUT 2: ', out_2)
    assert out_2 == '((a,((b,c),(d,e)))>0.7<0.9,(f,g));'


@pytest.fixture()
def multi_cali_tuple():
    cali_tuple_list = [
        ('a', 'b', '>0.1<0.2'),
        ('a', 'c', '>0.2<0.3'),
        ('a', 'e', '>0.3<0.4'),
        ('a', 'f', '>0.4<0.5'),
    ]
    return cali_tuple_list


def test_multi_calibration(multi_cali_tuple):
    cali_tuple_list = multi_cali_tuple
    out_str = multi_calibration(test_tree_1, cali_tuple_list)
    assert out_str == '((a, ((b, c), (d, e)))>0.3<0.4, (f, g))>0.4<0.5;'


@pytest.fixture()
def multi_cali_tuple_Cyano():
    cali_tuple_list = [
        ('Nostoc_azollae_0708', 'Nos8941', '>0.1<0.2'),
        ('Chroococcidiopsis_thermalis_PCC_7203',
         'Prochlorococcus_marinus_MIT_9313', '>0.2<0.3'),
        ('Ecoli_K12_DH10B', 'Met2661', '>0.3<0.4'),
        ('Nostoc_PCC_7107', 'Anabaena_90', '>0.4<0.5'),
        ('Nostoc_PCC_7107', 'Anabaena_90', '>0.5<0.6'),
    ]
    return cali_tuple_list


def test_multi_calibration_Cyano(multi_cali_tuple_Cyano):
    cali_tuple_list = multi_cali_tuple_Cyano
    out_str = multi_calibration(test_tree_2, cali_tuple_list)
    assert '>0.1<0.2' in out_str
    assert '>0.2<0.3' in out_str
    assert '>0.3<0.4' in out_str
    assert '>0.4<0.5' not in out_str
    assert '>0.5<0.6' in out_str


test_cali_ini = os.path.join(os.path.dirname(__file__), 'test_cali.ini')


def test_ParseConfig_init():
    p = ParseConfig(test_cali_ini)
    p.read_ini()
    assert p.cali_lines == ['cyano.nwk',
                            'Nostoc_azollae_0708, AnaXP35, >0.11<0.22',
                            'AnaMs2, Fis7414, >0.22<0.33',
                            'Cyanothece_PCC_7424, Synechococcus_sp._WH_8109,'
                            ' >0.33<0.44']


def test_ParseConfig_tree_file_name():
    p = ParseConfig(test_cali_ini)
    p.read_ini()
    # tree_file_name = p.tree_file_name
    # assert tree_file_name == 'cyano.nwk'
    assert p.cali_lines[0] == 'cyano.nwk'


def test_ParseConfig_tree_file_name_IOError():
    p = ParseConfig(test_cali_ini)
    p.read_ini()
    p.cali_lines[0] = p.cali_lines[0] + 'no_exist'
    with pytest.raises(IOError):
        p.tree_file_name


def test_ParseConfig_cali_list():
    p = ParseConfig(test_cali_ini)
    p.read_ini()
    cali_list = p.cali_list
    assert len(cali_list) == 3
    assert cali_list == [
        ['Nostoc_azollae_0708', 'AnaXP35', '>0.11<0.22'],
        ['AnaMs2', 'Fis7414', '>0.22<0.33'],
        ['Cyanothece_PCC_7424', 'Synechococcus_sp._WH_8109', '>0.33<0.44']
    ]


def test_ParseConfig_cali_list_ConfigFileSyntaxError():
    p = ParseConfig(test_cali_ini)
    p.read_ini()
    p.cali_lines[2] = 'AnaMs2, Fis7414, >0.22<0.33, error'
    with pytest.raises(ConfigFileSyntaxError):
        p.cali_list
    p.cali_lines[2] = 'AnaMs2, Fis7414'
    with pytest.raises(ConfigFileSyntaxError):
        p.cali_list


def test_get_tree_str():
    test_tree_nwk = os.path.join(os.path.dirname(__file__), 'test_tree.nwk')
    tree_str = get_tree_str(test_tree_nwk)
    assert tree_str == test_tree_2


def test_write_str_to_file():
    orig_tree_file = 'orig.test.nwk'
    write_str_to_file(orig_tree_file, 'This is a test.')
    assert os.path.isfile('orig.test.cali.nwk')
    with open('orig.test.cali.nwk', 'r') as f:
        assert f.read() == 'This is a test.'
    os.remove('orig.test.cali.nwk')
