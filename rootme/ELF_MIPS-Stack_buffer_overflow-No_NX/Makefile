CROSS_COMPILE   = mips-linux-gnu-
CC              = as
BIN             = ch65

LD              = ld
RM              = rm -f

all: $(BIN) post-build

$(BIN): $(BIN).o
	$(CROSS_COMPILE)$(LD) -o $@ $<

$(BIN).o: $(BIN).s
	$(CROSS_COMPILE)$(AS) -o $@ $<

clean:
	$(RM) $(BIN) $(BIN).o

post-build:
	chown -R app-systeme-$(BIN)-cracked:app-systeme-$(BIN) $(BIN).s $(BIN).o $(BIN) .passwd Makefile
	chmod -R o= .
	chmod 400 .passwd
	$(RM) $(BIN).o

.PHONY: all clean 
