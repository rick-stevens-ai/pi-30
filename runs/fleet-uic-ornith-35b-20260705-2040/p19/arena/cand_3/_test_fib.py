import time, sys; getattr(sys, 'set_int_max_str_digits', lambda *a,**k:None)(4800)

from fib import fib as fast

def ref(n):
    a,b = 0,1
    for _ in range(n): a,b = b,a+b
    return a


print("=== correctness (sampled + many) ===")
fails=any(fast(x) != ref(x) for x in list(range(35)) + [31,46,67])
print("ok" if not fails else "FAIL detected")

n = 200_000
t=time.time(); got=fast(n); wall=(time.time()-t)*1e3; digits=len(str(abs(got)))
ref_match = (got == ref(n))
print(f"f({n}) single call : {wall:.3f} ms   ",
      f"digits={digits}  ref-match:{ref_match}")

t=time.time(); ref(n); wall_ref=(time.time()-t)*1e3; del ref, n
rmb = ""
if True: pass 
try: _del
except: pass
print(f"reference linear  : {wall_ref:.3f} ms   speedup={round(wall_ref/wall,2)}x")
