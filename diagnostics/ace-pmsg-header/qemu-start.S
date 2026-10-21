.text
.global _start
_start:
 bl init_main
1: b 1b
.section .note.GNU-stack,"",%progbits
