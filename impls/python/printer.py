from mal_types import _is_atom,_is_false,_is_nil,_is_true,_is_vector,_list,_symbol,_vector,_is_list,_is_string,_is_symbol,_is_keyword,_keyword,_number,_hash_is_map,_u,str_types, _is_function
def _escape(s):
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

def pr_str(obj, print_readably=True):
    _r = print_readably
    if _is_list(obj):
        return '(' + ' '.join([pr_str(o, _r) for o in obj]) + ')'
    elif _is_vector(obj):
        return '[' + ' '.join([pr_str(o, _r) for o in obj]) + ']'
    elif _hash_is_map(obj):
        return (
            '{'
            + ' '.join(
                [f'{pr_str(k, _r)} {pr_str(v, _r)}' for k, v in obj.items()]
            )
            + '}'
        )
    elif type(obj) in str_types:
        if len(obj) > 0 and obj[0] == _u("\u029e"):
            return f':{obj[1:]}'
        elif print_readably:
            return f'"{_escape(obj)}"'
        else:
            return obj

    elif _is_nil(obj):
        return 'nil'
    elif _is_true(obj):
        return 'true'
    elif _is_false(obj):
        return 'false'

    elif _is_atom(obj):
        return f"(atom {pr_str(obj.val, _r)})"
    elif _is_function(obj):
        return "#<function>"
    else:
        return obj.__str__()