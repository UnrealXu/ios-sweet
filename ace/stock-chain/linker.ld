ENTRY(_start)
SECTIONS {
 . = 0;
 .text : { *(.text.boot) }
 /DISCARD/ : { *(.comment) *(.note*) *(.eh_frame*) }
}
