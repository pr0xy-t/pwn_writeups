.include "util.s"

.section	.rodata
.str1:
	.string 	"Hello!\n"

.section	.text
	.global	_start
	.type	_start, @function
_start:
	lea .str1(%rip), %rdi
	call put

	mov $77, %rdi
	call exit
