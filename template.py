from pwn import *

context.log_level = "debug"
LOCAL_LIBC = "/lib/x86_64-linux-gnu/libc.so.6"
REMOTE_LIBC = "./libc.so.6"
REMOTE_ADDR = "example.com"
REMOTE_PORT = 1337

elf = ELF("./level4")

if len(sys.argv) == 2:
    libc = ELF(LOCAL_LIBC)
    if sys.argv[1] == "l":
        sock = process(elf.path)
    elif sys.argv[1] == "d": # Debug
        gs = """
            break main
            continue
        """
        sock = gdb.debug(elf.path, gdbscript = gs)
else:
    libc = ELF(REMOTE_LIBC)
    sock = remote(REMOTE_ADDR, REMOTE_PORT)


if __name__ == "__main__":
    sock.interactive()



