/* SPDX-License-Identifier: MIT */
.file "ace-fdt-policy-start.S"
.text
.balign 4
.global _start
.type _start,%function
_start:
    mov x0,sp
    bl probe_main
    mov x8,#93
    svc #0
    brk #0
.size _start,.-_start
.section .note.GNU-stack,"",%progbits
