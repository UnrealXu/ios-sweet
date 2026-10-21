/* Host-only adapter. The DT parser, clock struct and identification functions
 * are inserted unchanged from the actual cached/patched XNU sources. Kernel
 * allocation, panic and CNTFRQ access are adapted; no hardware operation. */
#define _DEFAULT_SOURCE
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdarg.h>
#include <setjmp.h>
typedef uintptr_t vm_offset_t;
typedef size_t vm_size_t;
typedef uint64_t addr64_t;
#define SECURITY_READ_ONLY_LATE(x) x
#define Z_WAITOK 0
#define kalloc_type(t, flags) calloc(1, sizeof(t))
#define kfree_type(t, p) free(p)
static jmp_buf escape;
__attribute__((noreturn)) static void panic(const char *fmt, ...) { (void)fmt; longjmp(escape,1); }
static bool os_add3_overflow(uintptr_t a, uintptr_t b, uintptr_t c, uintptr_t *out)
{
    uintptr_t middle;
    return __builtin_add_overflow(a,b,&middle) || __builtin_add_overflow(middle,c,out);
}
static size_t test_strlcpy(char *out, const char *in, size_t size)
{
    size_t len = strlen(in);
    if (size) { size_t n = len < size-1 ? len : size-1; memcpy(out,in,n); out[n]=0; }
    return len;
}
#define strlcpy test_strlcpy
/* INSERT_DT_HEADER */
/* INSERT_DT_PARSER */
/* INSERT_CLOCK_STRUCT */
static clock_frequency_info_t gPEClockFrequencyInfo;
static char *gPESoCDeviceType;
static char gPESoCDeviceTypeBuffer[32];
static vm_offset_t gPESoCBasePhys;
static uint64_t counter_frequency;
#define SOC_DEVICE_TYPE_BUFFER_SIZE 32
typedef void boot_args;
vm_offset_t pe_arm_get_soc_base_phys(void);
#define __builtin_arm_rsr64(name) counter_frequency
/* INSERT_CLOCK_FUNCTIONS */
#undef __builtin_arm_rsr64
int test_xnu_clocks(const void *tree, size_t bytes, uint64_t counter, uint64_t *out)
{
    if (setjmp(escape)) return -1;
    gPESoCDeviceType = NULL;
    gPESoCBasePhys = 0;
    counter_frequency = counter;
    SecureDTInit(tree,bytes);
    pe_identify_machine(NULL);
    out[0] = pe_arm_get_soc_base_phys();
    out[1] = gPEClockFrequencyInfo.timebase_frequency_hz;
    out[2] = gPEClockFrequencyInfo.cpu_frequency_hz;
    out[3] = gPEClockFrequencyInfo.bus_frequency_hz;
    out[4] = gPEClockFrequencyInfo.bus_to_cpu_rate_num;
    out[5] = gPEClockFrequencyInfo.bus_to_cpu_rate_den;
    out[6] = gPEClockFrequencyInfo.bus_to_dec_rate_num;
    out[7] = gPEClockFrequencyInfo.bus_to_dec_rate_den;
    return 0;
}
int test_xnu_property(const void *tree, size_t bytes, const char *path, const char *name,
                      void *out, unsigned int capacity)
{
    if (setjmp(escape)) return -1;
    DTEntry entry;
    const void *value;
    unsigned int len;
    SecureDTInit(tree,bytes);
    if (SecureDTLookupEntry(NULL,path,&entry) != kSuccess ||
        SecureDTGetProperty(entry,name,&value,&len) != kSuccess || len > capacity) return -2;
    memcpy(out,value,len);
    return (int)len;
}
