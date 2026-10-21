/* SPDX-License-Identifier: MIT
 * Original, platform-independent read-only UFS wire encoder/response checker.
 * No MMIO, DMA mapping, cache maintenance, submission, SMC or storage access.
 */
#ifndef ACE_UFS_PROTOCOL_H
#define ACE_UFS_PROTOCOL_H
#include <stddef.h>
#include <stdint.h>

#define ACE_UFS_PRDT_MAX 16u
#define ACE_UFS_PRDT_CHUNK (256u * 1024u)
#define ACE_UFS_UPIU_REGION 512u
#define ACE_UFS_UCD_BYTES (2u * ACE_UFS_UPIU_REGION + 16u * ACE_UFS_PRDT_MAX)

enum ace_ufs_error {
    ACE_UFS_OK = 0, ACE_UFS_E_ARGUMENT = -1, ACE_UFS_E_RANGE = -2,
    ACE_UFS_E_COMMAND = -3, ACE_UFS_E_DMA = -4, ACE_UFS_E_OCS = -5,
    ACE_UFS_E_RESPONSE = -6, ACE_UFS_E_SCSI = -7
};
enum ace_ufs_identify {
    ACE_UFS_TEST_UNIT_READY, ACE_UFS_INQUIRY, ACE_UFS_READ_CAPACITY10,
    ACE_UFS_READ_CAPACITY16, ACE_UFS_REPORT_LUNS
};
struct ace_ufs_command { uint8_t cdb[16]; uint32_t transfer_bytes; uint8_t cdb_len; };
struct ace_ufs_utrd { uint8_t bytes[32]; };
struct ace_ufs_ucd { uint8_t bytes[ACE_UFS_UCD_BYTES]; };
struct ace_ufs_response {
    uint32_t residual_bytes;
    uint16_t sense_bytes;
    uint8_t scsi_status;
    const uint8_t *sense; /* borrowed from the caller's response buffer */
};

/* Zero-length reads are refused. block_bytes must be a power of 2, 512..65536.
 * Identify allocation: TUR=0, RC10=8, RC16=32, INQUIRY=4..252 (multiple of4),
 * REPORT_LUNS=16..4MiB (multiple of4). Only standard, non-EVPD INQUIRY. */
int ace_ufs_make_read10(uint64_t lba, uint32_t blocks, uint32_t block_bytes,
                      struct ace_ufs_command *out);
int ace_ufs_make_read16(uint64_t lba, uint32_t blocks, uint32_t block_bytes,
                      struct ace_ufs_command *out);
int ace_ufs_make_identify(enum ace_ufs_identify kind, uint32_t allocation,
                        struct ace_ufs_command *out);

/* Encode into caller-owned distinct output buffers. Ordinary LUN0..7; WLUN0x81 only for REPORT_LUNS.
 * UCD address must be128-byte aligned; data address/length 4-byte aligned.
 * Addresses are DEVICE DMA addresses, NOT assumed CPU physical addresses.
 * Caller must establish mapping/ownership/lifetime/cache coherence; this
 * function merely validates arithmetic, capability, nonoverlap and format.
 * data_dma is ignored for TUR. At most16 contiguous PRDs (4MiB). Outputs
 * remain unchanged on invalid input. No crypto extension/MCQ/UFSHCI4 support. */
int ace_ufs_encode(const struct ace_ufs_command *command, uint8_t lun,
                   uint8_t task_tag, uint64_t ucd_dma, uint64_t data_dma,
                   int dma64, struct ace_ufs_utrd *utrd, struct ace_ufs_ucd *ucd);

/* Caller must first synchronize DMA and supply actual available bytes.
 * EHS is unsupported; residual/overflow/underflow responses are refused for
 * block-read correctness. CHECK CONDITION returns E_SCSI with bounded sense
 * view populated. OCS must be the UTRD status nibble (no reserved bits).
 * Outputs are cleared on failure except E_SCSI, which provides sense/status. */
/* Bounded parsers for returned identification payloads. Capacity outputs are
 * unchanged on failure. RC10 last-LBA=0xffffffff returns E_RANGE: use RC16.
 * LUN parser accepts only simple peripheral LUN0..7 descriptors, rejects
 * duplicates/hierarchical/WLUN addresses rather than guessing a mapping. */
int ace_ufs_parse_capacity10(const uint8_t *data, size_t available,
                             uint64_t *blocks, uint32_t *block_bytes);
int ace_ufs_parse_capacity16(const uint8_t *data, size_t available,
                             uint64_t *blocks, uint32_t *block_bytes);
int ace_ufs_parse_luns(const uint8_t *data, size_t available, uint8_t *lun_mask);

int ace_ufs_check_response(uint8_t ocs, const uint8_t *response, size_t available,
                          uint8_t lun, uint8_t task_tag,
                          struct ace_ufs_response *out);
#endif
