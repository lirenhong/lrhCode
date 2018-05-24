def unpack_nest_dict_gen(d, pre=None):
    pre = pre[:] if pre else []
    for key, value in d.items():
        if not isinstance(value, dict):
                yield pre + [key]
        else:
            for v in unpack_dict_gen(value, pre + [key]):
                yield v
