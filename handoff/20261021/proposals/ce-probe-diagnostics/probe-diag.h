#ifndef ACE_CE_PROBE_DIAG_H
#define ACE_CE_PROBE_DIAG_H
#include <stdint.h>
/* Diagnostic observations only; never a CE authorization token. */
enum ace_ce_probe_field { ACE_CE_CURRENTEL, ACE_CE_DAIF, ACE_CE_ISAR0, ACE_CE_CPACR, ACE_CE_PROBE_FIELDS };
enum ace_ce_probe_rc { ACE_CE_PROBE_COMPLETE=0, ACE_CE_PROBE_EL=-1, ACE_CE_PROBE_DAIF=-2, ACE_CE_PROBE_SHA2=-3 };
int native_sha_ce_probe_diag(uint64_t observed[ACE_CE_PROBE_FIELDS]);
#endif
