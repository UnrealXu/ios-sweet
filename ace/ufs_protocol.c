/* SPDX-License-Identifier: MIT
 * Original implementation of public UFSHCI/UPIU and SCSI wire formats.
 * Layouts cross-checked against OnePlusOSS Linux ufs.h/ufshci.h (GPL-2.0);
 * no Linux driver implementation or GPL function bodies are incorporated.
 */
#include "ufs_protocol.h"

static void clear(void *ptr, size_t count)
{
    uint8_t *p = ptr;
    while (count--) *p++ = 0;
}
static void be16(uint8_t *p, uint16_t v) { p[0] = v >> 8; p[1] = v; }
static void be32(uint8_t *p, uint32_t v)
{
    p[0] = v >> 24; p[1] = v >> 16; p[2] = v >> 8; p[3] = v;
}
static void be64(uint8_t *p, uint64_t v) { be32(p, v >> 32); be32(p + 4, v); }
static void le32(uint8_t *p, uint32_t v)
{
    p[0] = v; p[1] = v >> 8; p[2] = v >> 16; p[3] = v >> 24;
}
static uint32_t get32(const uint8_t *p)
{
    return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 |
           (uint32_t)p[2] << 8 | p[3];
}
static uint64_t get64(const uint8_t *p) { return (uint64_t)get32(p) << 32 | get32(p + 4); }
static int block_valid(uint32_t bytes)
{
    return bytes >= 512 && bytes <= 65536 && !(bytes & (bytes - 1));
}
static int read_common(uint64_t lba, uint32_t blocks, uint32_t bytes)
{
    if (!blocks || !block_valid(bytes)) return ACE_UFS_E_ARGUMENT;
    if (lba > UINT64_MAX - (blocks - 1) || blocks > UINT32_MAX / bytes)
        return ACE_UFS_E_RANGE;
    return ACE_UFS_OK;
}
int ace_ufs_make_read10(uint64_t lba, uint32_t blocks, uint32_t bytes,
                      struct ace_ufs_command *out)
{
    int error = read_common(lba, blocks, bytes);
    if (!out) return ACE_UFS_E_ARGUMENT;
    if (error) return error;
    if (blocks > UINT16_MAX || lba > UINT32_MAX - (blocks - 1)) return ACE_UFS_E_RANGE;
    clear(out, sizeof(*out)); out->cdb[0] = 0x28; out->cdb_len = 10;
    be32(out->cdb + 2, (uint32_t)lba); be16(out->cdb + 7, (uint16_t)blocks);
    out->transfer_bytes = blocks * bytes;
    return ACE_UFS_OK;
}
int ace_ufs_make_read16(uint64_t lba, uint32_t blocks, uint32_t bytes,
                      struct ace_ufs_command *out)
{
    int error = read_common(lba, blocks, bytes);
    if (!out) return ACE_UFS_E_ARGUMENT;
    if (error) return error;
    clear(out, sizeof(*out)); out->cdb[0] = 0x88; out->cdb_len = 16;
    be64(out->cdb + 2, lba); be32(out->cdb + 10, blocks);
    out->transfer_bytes = blocks * bytes;
    return ACE_UFS_OK;
}
int ace_ufs_make_identify(enum ace_ufs_identify kind, uint32_t allocation,
                        struct ace_ufs_command *out)
{
    struct ace_ufs_command c;
    if (!out || (allocation & 3)) return ACE_UFS_E_ARGUMENT;
    clear(&c, sizeof(c)); c.transfer_bytes = allocation;
    switch (kind) {
    case ACE_UFS_TEST_UNIT_READY:
        if (allocation) return ACE_UFS_E_ARGUMENT;
        c.cdb_len = 6; break;
    case ACE_UFS_INQUIRY:
        if (allocation < 4 || allocation > 252) return ACE_UFS_E_RANGE;
        c.cdb[0] = 0x12; c.cdb[4] = allocation; c.cdb_len = 6; break;
    case ACE_UFS_READ_CAPACITY10:
        if (allocation != 8) return ACE_UFS_E_ARGUMENT;
        c.cdb[0] = 0x25; c.cdb_len = 10; break;
    case ACE_UFS_READ_CAPACITY16:
        if (allocation != 32) return ACE_UFS_E_ARGUMENT;
        c.cdb[0] = 0x9e; c.cdb[1] = 0x10; be32(c.cdb + 10, allocation); c.cdb_len = 16; break;
    case ACE_UFS_REPORT_LUNS:
        if (allocation < 16 || allocation > ACE_UFS_PRDT_MAX * ACE_UFS_PRDT_CHUNK)
            return ACE_UFS_E_RANGE;
        c.cdb[0] = 0xa0; be32(c.cdb + 6, allocation); c.cdb_len = 12; break;
    default: return ACE_UFS_E_COMMAND;
    }
    *out = c;
    return ACE_UFS_OK;
}
/* Do not let a caller replace a canonical read CDB with WRITE/UNMAP/etc. */
static int command_valid(const struct ace_ufs_command *c)
{
    struct ace_ufs_command expected;
    uint32_t n, bytes;
    int error;
    switch (c->cdb[0]) {
    case 0x28:
    case 0x88:
        n = c->cdb[0] == 0x28 ? ((uint32_t)c->cdb[7] << 8 | c->cdb[8]) : get32(c->cdb + 10);
        if (!n || c->transfer_bytes % n) return 0;
        bytes = c->transfer_bytes / n;
        error = c->cdb[0] == 0x28 ?
            ace_ufs_make_read10(get32(c->cdb + 2), n, bytes, &expected) :
            ace_ufs_make_read16(get64(c->cdb + 2), n, bytes, &expected);
        break;
    case 0x00: error = ace_ufs_make_identify(ACE_UFS_TEST_UNIT_READY, c->transfer_bytes, &expected); break;
    case 0x12: error = ace_ufs_make_identify(ACE_UFS_INQUIRY, c->transfer_bytes, &expected); break;
    case 0x25: error = ace_ufs_make_identify(ACE_UFS_READ_CAPACITY10, c->transfer_bytes, &expected); break;
    case 0x9e: error = ace_ufs_make_identify(ACE_UFS_READ_CAPACITY16, c->transfer_bytes, &expected); break;
    case 0xa0: error = ace_ufs_make_identify(ACE_UFS_REPORT_LUNS, c->transfer_bytes, &expected); break;
    default: return 0;
    }
    if (error || expected.cdb_len != c->cdb_len) return 0;
    for (unsigned i = 0; i < 16; i++) if (expected.cdb[i] != c->cdb[i]) return 0;
    return 1;
}
static int dma_range(uint64_t base, uint32_t size, int dma64)
{
    if (!size || base > UINT64_MAX - (size - 1)) return 0;
    return dma64 || base + size - 1 <= UINT32_MAX;
}
int ace_ufs_encode(const struct ace_ufs_command *c, uint8_t lun, uint8_t tag,
                   uint64_t ucd_dma, uint64_t data_dma, int dma64,
                   struct ace_ufs_utrd *utrd, struct ace_ufs_ucd *ucd)
{
    uint32_t len, entries, remaining;
    uint64_t address;
    if (!c || !utrd || !ucd || (dma64 != 0 && dma64 != 1)) return ACE_UFS_E_ARGUMENT;
    if (lun > 7 && !(lun == 0x81 && c->cdb[0] == 0xa0)) return ACE_UFS_E_ARGUMENT;
    if (!command_valid(c)) return ACE_UFS_E_COMMAND;
    len = c->transfer_bytes;
    if (len > ACE_UFS_PRDT_MAX * ACE_UFS_PRDT_CHUNK) return ACE_UFS_E_RANGE;
    if ((ucd_dma & 127) || !dma_range(ucd_dma, ACE_UFS_UCD_BYTES, dma64)) return ACE_UFS_E_DMA;
    if (len && ((data_dma & 3) || (len & 3) || !dma_range(data_dma, len, dma64))) return ACE_UFS_E_DMA;
    if (len && data_dma <= ucd_dma + ACE_UFS_UCD_BYTES - 1 && ucd_dma <= data_dma + len - 1)
        return ACE_UFS_E_DMA;
    clear(utrd, sizeof(*utrd)); clear(ucd, sizeof(*ucd));
    le32(utrd->bytes, 0x11000000u | (len ? 0x04000000u : 0)); /* CT=UFS, IOC, DD */
    le32(utrd->bytes + 8, 0x0f); /* invalid OCS until controller completes */
    le32(utrd->bytes + 16, (uint32_t)ucd_dma); le32(utrd->bytes + 20, ucd_dma >> 32);
    le32(utrd->bytes + 24, (128u << 16) | 128u); /* response offset/length DWORDs */
    entries = (len + ACE_UFS_PRDT_CHUNK - 1) / ACE_UFS_PRDT_CHUNK;
    le32(utrd->bytes + 28, (256u << 16) | entries);
    ucd->bytes[0] = 0x01; ucd->bytes[1] = len ? 0x40 : 0;
    ucd->bytes[2] = lun; ucd->bytes[3] = tag;
    be32(ucd->bytes + 12, len);
    for (unsigned i = 0; i < 16; i++) ucd->bytes[16 + i] = c->cdb[i];
    remaining = len; address = data_dma;
    for (uint32_t i = 0; i < entries; i++) {
        uint8_t *p = ucd->bytes + 2 * ACE_UFS_UPIU_REGION + 16 * i;
        uint32_t chunk = remaining > ACE_UFS_PRDT_CHUNK ? ACE_UFS_PRDT_CHUNK : remaining;
        le32(p, (uint32_t)address); le32(p + 4, address >> 32); le32(p + 12, chunk - 1);
        remaining -= chunk; address += chunk;
    }
    return ACE_UFS_OK;
}
int ace_ufs_check_response(uint8_t ocs, const uint8_t *r, size_t available,
                          uint8_t lun, uint8_t tag, struct ace_ufs_response *out)
{
    uint16_t segment, sense;
    if (!out) return ACE_UFS_E_ARGUMENT;
    clear(out, sizeof(*out));
    if (ocs) return ACE_UFS_E_OCS;
    if (!r || available < 32 || (lun > 7 && lun != 0x81)) return ACE_UFS_E_ARGUMENT;
    if (r[0] != 0x21 || r[2] != lun || r[3] != tag || r[6] || r[8]) return ACE_UFS_E_RESPONSE;
    /* Reject overflow/underflow flags and nonzero residual even for GOOD. */
    if ((r[1] & 0x60) || get32(r + 12)) return ACE_UFS_E_RESPONSE;
    segment = (uint16_t)r[10] << 8 | r[11];
    if ((size_t)segment > available - 32) return ACE_UFS_E_RESPONSE;
    sense = 0;
    if (segment) {
        if (segment < 2) return ACE_UFS_E_RESPONSE;
        sense = (uint16_t)r[32] << 8 | r[33];
        if (sense > segment - 2) return ACE_UFS_E_RESPONSE;
    }
    out->scsi_status = r[7]; out->sense_bytes = sense;
    out->sense = sense ? r + 34 : NULL;
    return r[7] ? ACE_UFS_E_SCSI : ACE_UFS_OK;
}

int ace_ufs_parse_capacity10(const uint8_t *data, size_t available,
                             uint64_t *blocks, uint32_t *bytes)
{
    uint32_t last, size;
    if (!data || !blocks || !bytes || available < 8) return ACE_UFS_E_ARGUMENT;
    last = get32(data); size = get32(data + 4);
    if (last == UINT32_MAX) return ACE_UFS_E_RANGE;
    if (!block_valid(size)) return ACE_UFS_E_RESPONSE;
    *blocks = (uint64_t)last + 1; *bytes = size;
    return ACE_UFS_OK;
}
int ace_ufs_parse_capacity16(const uint8_t *data, size_t available,
                             uint64_t *blocks, uint32_t *bytes)
{
    uint64_t last;
    uint32_t size;
    if (!data || !blocks || !bytes || available < 32) return ACE_UFS_E_ARGUMENT;
    last = get64(data); size = get32(data + 8);
    if (last == UINT64_MAX) return ACE_UFS_E_RANGE;
    if (!block_valid(size)) return ACE_UFS_E_RESPONSE;
    *blocks = last + 1; *bytes = size;
    return ACE_UFS_OK;
}
int ace_ufs_parse_luns(const uint8_t *data, size_t available, uint8_t *lun_mask)
{
    uint32_t length;
    uint8_t mask = 0;
    if (!data || !lun_mask || available < 8) return ACE_UFS_E_ARGUMENT;
    length = get32(data);
    if ((length & 7) || length > 64 || length > available - 8) return ACE_UFS_E_RESPONSE;
    for (size_t i = 8; i < (size_t)length + 8; i += 8) {
        uint8_t lun = data[i + 1];
        if (data[i] || lun > 7 || (mask & (1u << lun))) return ACE_UFS_E_RESPONSE;
        for (unsigned j = 2; j < 8; j++) if (data[i + j]) return ACE_UFS_E_RESPONSE;
        mask |= (uint8_t)(1u << lun);
    }
    *lun_mask = mask;
    return ACE_UFS_OK;
}
