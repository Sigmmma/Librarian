from hamcrest import *
from pocha import before, beforeEach, describe, it

from binilla.constants import VISIBILITY_HIDDEN
from reclaimer.common_descs import Float, SInt32, UInt32, Struct
from supyr_struct.defs.block_def import BlockDef

import dictionizer

@describe('Dictionizer Tests')
def dictionizerTests():

    test_desc = Struct("testblock",
        Float("some_float"),
        Float("some_other_float"),
        Float("scaled_float", UNIT_SCALE=30.0),
        SInt32("some_int"),
        SInt32("some_other_int"),
        SInt32("scaled_int", UNIT_SCALE=30),
        Struct("sub",
            UInt32("rule"),
            UInt32("nice"),
        ),
        Float("invisible_float", VISIBLE=VISIBILITY_HIDDEN),
    )

    test_def = BlockDef(test_desc)

    def buildTestBlock():

        global test_block
        global test_dict

        test_dict = {
            'some_float' : 1.0,
            'some_other_float' : 6.0,
            'scaled_float' : 2.0 * 30.0,
            'some_int' : 0,
            'some_other_int' : -5,
            'scaled_int' : 25 * 30,
            'sub' : {
                'rule' : 34,
                'nice' : 69
            }
        }

        test_block = test_def.build()

        test_block.some_float       = test_dict['some_float']
        test_block.some_other_float = test_dict['some_other_float']
        test_block.scaled_float     = test_dict['scaled_float'] / 30.0
        test_block.some_int         = test_dict['some_int']
        test_block.some_other_int   = test_dict['some_other_int']
        test_block.scaled_int       = test_dict['scaled_int'] / 30
        test_block.sub.rule         = test_dict['sub']['rule']
        test_block.sub.nice         = test_dict['sub']['nice']

    @before
    def beforeAll():
        buildTestBlock()

    @describe('block_to_dict')
    def BlockToDict():

        @it('Converts basic definition to dict')
        def basicConvert():
            result_dict = dictionizer.block_to_dict(test_block)

            assert_that(result_dict, equal_to(test_dict))

        @it('Leaves out invisibles')
        def noInvis():
            result_dict = dictionizer.block_to_dict(test_block)

            assert_that(result_dict.get('invisible_float', None), none())

        @it('Handles unit scaling')
        def noInvis():
            result_dict = dictionizer.block_to_dict(test_block)

            scaling_one = test_block.desc[
                test_block.desc['NAME_MAP']['scaled_float']
                ]['UNIT_SCALE']
            scaling_two = test_block.desc[
                test_block.desc['NAME_MAP']['scaled_int']
                ]['UNIT_SCALE']

            assert_that(
                result_dict['scaled_float'],
                equal_to(test_block.scaled_float * scaling_one)
            )
            assert_that(
                result_dict['scaled_int'],
                equal_to(test_block.scaled_int * scaling_two)
            )
