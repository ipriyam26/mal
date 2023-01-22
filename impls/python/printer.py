def pr_str(obj, print_readably=True):
    if isinstance(obj, list):
        return "(" + " ".join(pr_str(x, print_readably) for x in obj) + ")"
    elif isinstance(obj, str):
        if len(obj) > 0 and obj[0] == '\u029e':
            return f':{obj[1:]}'
        elif print_readably:
            return '"' + obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + '"'
        # elif types._nil_Q(obj):
        #     return "nil"
        # elif types._true_Q(obj):
        #     return "true"
        # elif types._false_Q(obj):
        #     return "false"
        # elif types._atom_Q(obj):
        #     return "(atom " + _pr_str(obj.val,_r) + ")"
        # else:
        #     return obj.__str__()
        else:
            return obj
        # return obj if print_readably else obj.
        # return str(obj)