/* Host guard pages and sanitizer validation for the actual kernel ring core. */
#define _GNU_SOURCE
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <pexpert/arm/ace_pmsg.h>

static uint32_t rng = 6895;
static uint32_t next(void)
{
    rng ^= rng << 13;
    rng ^= rng >> 17;
    return rng ^= rng << 5;
}
int main(void)
{
    enum { guard = 4096 };
    uint8_t *mapping = mmap(NULL, ACE_PMSG_BYTES + 2 * guard,
                            PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    assert(mapping != MAP_FAILED);
    assert(mprotect(mapping, guard, PROT_NONE) == 0);
    assert(mprotect(mapping + guard + ACE_PMSG_BYTES, guard, PROT_NONE) == 0);
    uint8_t *zone = mapping + guard;
    uint32_t *header = (uint32_t *)zone;
    memset(zone, 0, ACE_PMSG_BYTES);
    header[0] = ACE_PMSG_SIGNATURE;
    struct ace_pmsg_console console = {0};
    assert(ace_pmsg_console_bind(&console, zone, ACE_PMSG_BYTES) == 0);
    uint32_t count = 3 * ACE_PMSG_CAPACITY + 17;
    for (uint32_t i = 0; i < count; i++) {
        assert(ace_pmsg_console_putc(&console, (uint8_t)i) == 0);
    }
    assert(header[1] == 17 && header[2] == ACE_PMSG_CAPACITY);
    for (uint32_t i = 0; i < ACE_PMSG_CAPACITY; i++) {
        assert(zone[12 + (header[1] + i) % ACE_PMSG_CAPACITY] == (uint8_t)(count - ACE_PMSG_CAPACITY + i));
    }
    uint8_t *before = malloc(ACE_PMSG_BYTES);
    assert(before);
    for (unsigned i = 0; i < 1024; i++) {
        header[0] = next() % 4 ? ACE_PMSG_SIGNATURE : 0;
        header[1] = next() % (ACE_PMSG_CAPACITY + 16);
        header[2] = next() % (ACE_PMSG_CAPACITY + 16);
        if (i % 3 == 0) header[2] = ACE_PMSG_CAPACITY;
        if (i % 3 == 1) header[2] = header[1];
        memcpy(before, zone, ACE_PMSG_BYTES);
        struct ace_pmsg_console candidate = {0};
        int valid = header[0] == ACE_PMSG_SIGNATURE && header[1] < ACE_PMSG_CAPACITY &&
                    header[2] <= ACE_PMSG_CAPACITY &&
                    (header[2] == ACE_PMSG_CAPACITY || header[1] == header[2]);
        assert((ace_pmsg_console_bind(&candidate, zone, ACE_PMSG_BYTES) == 0) == valid);
        assert(memcmp(before, zone, ACE_PMSG_BYTES) == 0);
        if (valid) {
            candidate.busy = 1;
            assert(ace_pmsg_console_putc(&candidate, 42) == ACE_PMSG_BUSY);
            assert(memcmp(before, zone, ACE_PMSG_BYTES) == 0);
            candidate.busy = 0;
            assert(ace_pmsg_console_putc(&candidate, 42) == 0);
            assert(candidate.busy == 0);
        } else {
            struct ace_pmsg_console empty = {0};
            assert(memcmp(&candidate, &empty, sizeof(empty)) == 0);
        }
    }
    free(before);
    assert(munmap(mapping, ACE_PMSG_BYTES + 2 * guard) == 0);
    return 0;
}
