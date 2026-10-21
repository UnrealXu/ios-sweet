ENTRY(_start)
SECTIONS {
 . = 0;
 .text : { KEEP(*(.text.boot)) *(.text*) }
 .rodata : { *(.rodata*) }
 .data : { *(.data*) }
 . = ALIGN(16);
 __bss_start = .;
 .bss (NOLOAD) : { *(.bss*) *(COMMON) }
 . = ALIGN(16);
 __bss_end = .;
 . = ALIGN(4096);
 image_end = .;
 /DISCARD/ : { *(.note*) *(.comment*) *(.eh_frame*) }
}
