NO_ISSUES

## Notes (informational, not flagged as race issues)

- `value()` reads `_n` without the lock. On CPython every bytecode boundary is GIL-held and Python int reads are unconditionally atomic, so concurrent readers never observe torn data — there is no practical race to fix here.
- Some might call for wrapping `value()` in `with self._lock`. That's a defensive API-polish change, not a real race fix, so it stays out of the verdict.
