CHALLENGE=$(shell basename $(shell pwd))
USER=app-systeme-$(CHALLENGE)
USER_CRACKED=app-systeme-$(CHALLENGE)-cracked

CC=gcc
CFLAGS=-Wl,-z,norelro -fno-stack-protector
LDFLAGS=

SRC=$(CHALLENGE).c
OBJ=$(SRC:.c=.o)
BIN=$(CHALLENGE)

.DEFAULT_GOAL := challenge
.PHONY : clean all

pre-build:
	@echo "Removing immutable flags..."
	chattr -R -i .

post-build:
	@echo "Adding immutable flags..."
	chattr -R +i .

all: pre-build
	@echo "Compiling..."
	$(MAKE) $(BIN)

$(BIN): $(OBJ)
	$(CC) -o $@ $(SRC) $(LDFLAGS) $(CFLAGS)

challenge: all
	@echo "Applying permissions..."
	rm -f $(OBJ)
	chown $(USER_CRACKED):$(USER) . $(BIN) $(BIN).c Makefile
	chown $(USER_CRACKED):root .passwd
	chmod 400 .passwd
	chmod 444 $(SRC) Makefile
	chmod 550 $(BIN)
	chmod u+s $(BIN)
	$(MAKE) post-build

clean: pre-build
	rm -f $(BIN) $(OBJ)
	$(MAKE) post-build

