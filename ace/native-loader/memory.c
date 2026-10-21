/* SPDX-License-Identifier: MIT */
/* GCC can lower aligned local aggregate initialization to memcpy even with
 * -ffreestanding/-fno-builtin (notably with -mstrict-align). Supply the real
 * freestanding ABI operation, with exact bounds and no recursive builtin. */
#include <stddef.h>
void *memcpy(void *destination,const void *source,size_t bytes) {
    volatile unsigned char *d=destination;
    const volatile unsigned char *s=source;
    for(size_t i=0;i<bytes;i++) d[i]=s[i];
    return destination;
}
