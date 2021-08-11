#! /bin/sh
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

cd /challenge/app-systeme/ch65/

export QEMU_LD_PREFIX=/usr/mips-linux-gnu
timeout --foreground -k10s 600s /opt/qemu/mips-linux-user/qemu-mips -noaslr ./ch65
