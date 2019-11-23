from supyr_struct.blocks.block import Block
from binilla.constants import VISIBILITY_SHOWN

def block_to_dict(block):
    '''Returns all key and value pairs of reclaimer block as a dictionary'''
    dic = dict()

    desc = block.desc

    for idx, name in enumerate(desc["NAME_MAP"]):
        item = block[idx]

        # Skip hidden blocks.
        if desc[idx].get("VISIBLE", VISIBILITY_SHOWN) != VISIBILITY_SHOWN:
            continue

        # if a block, call this same method on it to also convert it to a dict.
        if isinstance(item, Block):
            item = to_dict(item)
        # If primitive type handle generically.
        else:
            item *= desc[idx].get("UNIT_SCALE", 1)
            # Turn number into compact notation if float
            if isinstance(item, float):
                item = float("%g" % (item))

        dic[name] = item

    return dic
