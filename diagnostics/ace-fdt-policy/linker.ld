/* Linux EL0 executable. Keep the zero-file-size BSS LOAD page-aligned: a
 * partial initial page beyond EOF is not a valid file-backed mapping. */
ENTRY(_start)
PHDRS {
 text PT_LOAD FILEHDR PHDRS FLAGS(5);
 data PT_LOAD FLAGS(6);
 stack PT_GNU_STACK FLAGS(6);
}
SECTIONS {
 . = 0x400000 + SIZEOF_HEADERS;
 .text : { *(.text*) } :text
 .rodata : { *(.rodata*) } :text
 . = ALIGN(0x10000);
 .data : { *(.data*) } :data
 .bss (NOLOAD) : { *(.bss*) *(COMMON) } :data
 /DISCARD/ : { *(.note*) *(.comment*) *(.eh_frame*) }
}
