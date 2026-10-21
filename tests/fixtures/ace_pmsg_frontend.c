/* Host-only adapter for the actual XNU serial frontend. No device access.
 * ARM register reads, address mapping and completion instructions are stubs;
 * the frontend control flow and ring implementation come from the patch. */
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <pexpert/arm/ace_pmsg.h>
/* INSERT_ACE_BOOT_ARGS */
struct probe_input {
    uint64_t ram_base, ram_bytes, pmsg_base, pmsg_bytes, sctlr, current_el;
    uint32_t revision, version, bootarg_present, enabled, lookup_ok, compat_ok;
    uint32_t reg_length, ecc_size, type_signature, ecc_length, type_length, map_ok;
};
struct probe_stats {
    uint32_t maps, registrations, completions;
    uint64_t map_base, map_bytes;
};
static struct probe_input input;
static struct probe_stats stats;
static uint8_t *mapped_zone;
static boot_args args;
static struct { void *bootArgs; } PE_state;
typedef void *DTEntry;
#define kSuccess 0
#define SECURITY_READ_ONLY_LATE(x) x
#define SERIAL_ACE_PMSG 0x40
struct pe_serial_functions {
    void (*init)(void);
    unsigned int (*transmit_ready)(void);
    unsigned int (*receive_ready)(void);
    void (*transmit_data)(uint8_t);
    uint8_t (*receive_data)(void);
    unsigned int device;
};
static struct pe_serial_functions *registered;
static void register_serial_functions(struct pe_serial_functions *f)
{
    registered = f;
    stats.registrations++;
}
static int PE_parse_boot_argn(const char *name, void *out, int bytes)
{
    if (strcmp(name, "ace_pmsg") || bytes != 4 || !input.bootarg_present) return 0;
    memcpy(out, &input.enabled, 4);
    return 1;
}
static int SecureDTLookupEntry(void *root, const char *path, DTEntry *out)
{
    if (root || strcmp(path, "/chosen/ace-pmsg") || !input.lookup_ok) return -1;
    *out = &input;
    return 0;
}
static int SecureDTGetProperty(DTEntry entry, const char *name, const void **out, unsigned int *bytes)
{
    static const char good[] = "ace,ramoops-pmsg-v1";
    static const char bad[sizeof(good)] = "incorrect";
    static uint64_t reg[2];
    if (entry != &input) return -1;
    if (!strcmp(name, "compatible")) {
        *out = input.compat_ok ? good : bad;
        *bytes = sizeof(good);
    } else if (!strcmp(name, "reg")) {
        reg[0] = input.pmsg_base;
        reg[1] = input.pmsg_bytes;
        *out = reg;
        *bytes = input.reg_length;
    } else if (!strcmp(name, "ecc-size")) {
        *out = &input.ecc_size;
        *bytes = input.ecc_length;
    } else if (!strcmp(name, "type-signature")) {
        *out = &input.type_signature;
        *bytes = input.type_length;
    } else return -1;
    return 0;
}
static void *ml_io_map_wcomb(uint64_t address, uint64_t bytes)
{
    stats.maps++;
    stats.map_base = address;
    stats.map_bytes = bytes;
    return input.map_ok ? mapped_zone : NULL;
}
static uint64_t test_register(const char *name)
{
    return !strcmp(name, "CurrentEL") ? input.current_el : input.sctlr;
}
static void test_completion(void) { stats.completions++; }
#define __builtin_arm_rsr64(name) test_register(name)
/* Replace only the inline assembly expression in this host translation unit.
 * Function-like volatile(...) does not alter volatile pointer declarations. */
#define __asm__
#define volatile(...) test_completion()
/* INSERT_ACE_FRONTEND */
#undef __asm__
#undef volatile
#undef __builtin_arm_rsr64
void test_probe(const struct probe_input *given, uint8_t *zone, struct probe_stats *out)
{
    input = *given;
    memset(&stats, 0, sizeof(stats));
    memset(&ace_pmsg_console, 0, sizeof(ace_pmsg_console));
    memset(&args, 0, sizeof(args));
    args.Revision = given->revision;
    args.Version = given->version;
    args.physBase = given->ram_base;
    args.memSize = given->ram_bytes;
    PE_state.bootArgs = &args;
    mapped_zone = zone;
    registered = NULL;
    ace_pmsg_probe();
    *out = stats;
}
void test_send(uint8_t byte) { if (registered) registered->transmit_data(byte); }
unsigned int test_ready(void) { return registered ? registered->transmit_ready() : 0; }
void test_busy(unsigned int value) { ace_pmsg_console.busy = value; }
