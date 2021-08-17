# Libs

Using qemu's usermode emulation, it is possible to run the target binary with a specific glibc version.

This folder contains various versions of glibc and ld, and these debugging symbols file.

The version of these libraries are often seen in pwn problems.


# Usage
```python
from pwn import *

elf = ELF("target-binary")
libc = ELF("./sysroot/lib/x86_64-linux-gnu/libc.so.6")

script = '\n'.join([
	"set sysroot ./sysroot",
	"break main",
# and so on...
	"continue",
])

p = gdb.debug( elf.path, sysroot = "./sysroot", gdbscript = script )

# write someting...

p.interactive()
```
**If glibc symbol information is not loaded, run "set sysroot ./sysroot" in the gdb window when you first break.**
![set sysroot ./sysroot](https://raw.githubusercontent.com/pr0xy-t/pwn_writeups/master/libs/sysroot.png "sysroot.png")

# Collected files

* libc6 2.23-0ubuntu11 (amd64 binary)
	* sha256: 74ca69ada4429ae5fce87f7e3addb56f1b53964599e8526244fecd164b3c4b44

* libc6 2.27-3ubuntu1 (amd64 binary)
	* sha256: cd7c1a035d24122798d97a47a10f6e2b71d58710aecfd392375f1aa9bdde164d

