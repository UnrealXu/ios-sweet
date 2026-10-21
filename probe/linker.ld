ENTRY(_start)
SECTIONS
{
    . = 0;
    .text : { KEEP(*(.text.boot)) *(.text*) }
    .rodata : { *(.rodata*) }
    .data : { *(.data*) }
    /* Include zeroed stack in raw image: no reliance on loader clearing BSS. */
    .bss : { *(.bss*) *(COMMON) }
    . = ALIGN(4096);
    image_end = .;
    /DISCARD/ : { *(.comment) *(.note*) *(.eh_frame*) }
}
