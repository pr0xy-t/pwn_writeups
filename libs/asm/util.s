.include "inc/syscall_x86_64.inc"



# put(data)
put:
	push %rdi
	push %rsi
	call strlen
	mov %rax, %rdx	
	mov %rdi, %rsi
	mov $1, %rdi
	mov $sys_write, %rax
	syscall

	pop %rsi
	pop %rdi
	ret

# strlen(data)
strlen:
	push %rdi
	mov $0xffffffff, %ecx
	mov $0, %eax
	repne scasb
	mov %ecx, %eax
	not %eax
	sub $1,%eax
	pop %rdi
	ret
	


# exit(status_number)
exit:
	mov $sys_exit, %rax
	syscall
