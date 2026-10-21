/* SPDX-License-Identifier: MIT */
#include "pstore_ring.h"

static int span_ok(const void *p, size_t n)
{
    return (!n || p) && (!n || (uintptr_t)p <= UINTPTR_MAX - n);
}

/* Integer comparisons avoid ordering unrelated C object pointers. Call only
 * after span_ok; zero-length ranges never overlap. */
static int overlaps(const void *a, size_t an, const void *b, size_t bn)
{
    return an && bn && (uintptr_t)a < (uintptr_t)b + bn &&
           (uintptr_t)b < (uintptr_t)a + an;
}

static uint32_t load_le32(const unsigned char *p)
{
    return (uint32_t)p[0] | (uint32_t)p[1] << 8 |
           (uint32_t)p[2] << 16 | (uint32_t)p[3] << 24;
}

static void store_le32(unsigned char *p, uint32_t v)
{
    p[0] = (unsigned char)v;
    p[1] = (unsigned char)(v >> 8);
    p[2] = (unsigned char)(v >> 16);
    p[3] = (unsigned char)(v >> 24);
}

static int inspect(const void *zone, size_t bytes,
                   struct ace_pstore_ring_info *state)
{
    const unsigned char *p = zone;
    size_t cap;
    if (!zone || bytes <= ACE_PSTORE_RING_HEADER_BYTES)
        return ACE_PSTORE_RING_E_ARGUMENT;
    cap = bytes - ACE_PSTORE_RING_HEADER_BYTES;
    if (cap > INT32_MAX || !span_ok(zone, bytes))
        return ACE_PSTORE_RING_E_RANGE;
    if (load_le32(p) != ACE_PSTORE_RING_SIGNATURE)
        return ACE_PSTORE_RING_E_HEADER;
    state->capacity = cap;
    state->start = load_le32(p + 4);
    state->size = load_le32(p + 8);
    if (state->size > cap || state->start > state->size)
        return ACE_PSTORE_RING_E_HEADER;
    return ACE_PSTORE_RING_OK;
}

int ace_pstore_ring_validate(const void *zone, size_t zone_bytes,
                            struct ace_pstore_ring_info *info)
{
    struct ace_pstore_ring_info state;
    int e = inspect(zone, zone_bytes, &state);
    if (e)
        return e;
    if (info) {
        if ((uintptr_t)info % _Alignof(struct ace_pstore_ring_info))
            return ACE_PSTORE_RING_E_ARGUMENT;
        if (!span_ok(info, sizeof(*info)))
            return ACE_PSTORE_RING_E_RANGE;
        if (overlaps(zone, zone_bytes, info, sizeof(*info)))
            return ACE_PSTORE_RING_E_ALIAS;
        info->capacity = state.capacity;
        info->start = state.start;
        info->size = state.size;
    }
    return ACE_PSTORE_RING_OK;
}

int ace_pstore_ring_append(void *zone, size_t zone_bytes,
                          const void *source, size_t source_bytes)
{
    struct ace_pstore_ring_info state;
    unsigned char *data;
    const unsigned char *s = source;
    size_t count, cursor, i;
    uint32_t size, start;
    int e = inspect(zone, zone_bytes, &state);
    if (e)
        return e;
    if (!source && source_bytes)
        return ACE_PSTORE_RING_E_ARGUMENT;
    if (!span_ok(source, source_bytes))
        return ACE_PSTORE_RING_E_RANGE;
    if (overlaps(zone, zone_bytes, source, source_bytes))
        return ACE_PSTORE_RING_E_ALIAS;
    if (!source_bytes)
        return ACE_PSTORE_RING_OK;
    if ((state.size < state.capacity && state.start != state.size) ||
        state.start >= state.capacity)
        return ACE_PSTORE_RING_E_STATE;
    count = source_bytes < state.capacity ? source_bytes : state.capacity;
    s += source_bytes - count;
    size = (uint32_t)(count > state.capacity - state.size ?
                     state.capacity : state.size + count);
    data = (unsigned char *)zone + ACE_PSTORE_RING_HEADER_BYTES;
    cursor = state.start;
    for (i = 0; i < count; ++i) {
        data[cursor++] = s[i];
        if (cursor == state.capacity)
            cursor = 0;
    }
    start = (uint32_t)cursor;
    /* Completed-call bytes match persistent_ram_write. This is ordinary RAM,
     * not an atomic/crash-safe publication or a cache persistence protocol. */
    store_le32((unsigned char *)zone + 4, start);
    store_le32((unsigned char *)zone + 8, size);
    return ACE_PSTORE_RING_OK;
}

int ace_pstore_ring_read(const void *zone, size_t zone_bytes,
                        void *out, size_t out_bytes, size_t *written)
{
    struct ace_pstore_ring_info state;
    const unsigned char *data;
    unsigned char *dst = out;
    size_t i, first;
    int e = inspect(zone, zone_bytes, &state);
    if (e)
        return e;
    if (!written || (!out && out_bytes) ||
        (uintptr_t)written % _Alignof(size_t))
        return ACE_PSTORE_RING_E_ARGUMENT;
    if (!span_ok(out, out_bytes) || !span_ok(written, sizeof(*written)))
        return ACE_PSTORE_RING_E_RANGE;
    if (overlaps(zone, zone_bytes, out, out_bytes) ||
        overlaps(zone, zone_bytes, written, sizeof(*written)) ||
        overlaps(out, out_bytes, written, sizeof(*written)))
        return ACE_PSTORE_RING_E_ALIAS;
    if (out_bytes < state.size)
        return ACE_PSTORE_RING_E_SPACE;
    data = (const unsigned char *)zone + ACE_PSTORE_RING_HEADER_BYTES;
    first = state.size - state.start;
    for (i = 0; i < first; ++i)
        dst[i] = data[state.start + i];
    for (i = 0; i < state.start; ++i)
        dst[first + i] = data[i];
    *written = state.size;
    return ACE_PSTORE_RING_OK;
}
