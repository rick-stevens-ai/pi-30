import importlib.util
import importlib.machinery
import sysconfig

def _load_std_decimal():
    stdlib_dir = sysconfig.get_path('stdlib')
    spec = importlib.machinery.PathFinder.find_spec('decimal', [stdlib_dir])
    std_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(std_mod)
    return std_mod.Decimal, std_mod.getcontext

_StdDecimal,_getcontext=_load_std_decimal()

class Decimal(_StdDecimal):
    def __sub__(self, other):
        print('in custom sub')
        try:
            return super().__sub__(other)
        except Exception as e:
            print('except', e)
            return super().__sub__(_StdDecimal(other))

# test 
a=Decimal(1); b=a-2.0; print(b)
