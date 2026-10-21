/* SPDX-License-Identifier: MIT */
#ifndef ACE_PSTORE_HANDOFF_H
#define ACE_PSTORE_HANDOFF_H
#include "pstore_trial.h"
/* Optional boundary evidence in an already owned/excluded pmsg zone. Never
 * seeds RAM or treats absence of evidence as proof of no Android execution. */
static uint64_t ace_handoff_word(const uint8_t *p) {
    uint64_t v=0;for(unsigned i=0;i<8;i++)v|=(uint64_t)p[i]<<(8*i);return v;
}
static int ace_pstore_android_handoff(void *zone,size_t bytes,const char token[17],
                                     const uint8_t *record,size_t length) {
    if(!record || length!=288)return -1;
    int pending=ace_pstore_trial_pending(zone,bytes,token);
    if(pending!=1)return pending<0?pending:-5;
    static const char magic[]="ACEFALL1";
    for(unsigned i=0;i<8;i++)if(record[i]!=(uint8_t)magic[i])return -1;
    for(unsigned i=0;i<17;i++)if(record[8+i]!=(uint8_t)token[i])return -1;
    for(unsigned i=25;i<32;i++)if(record[i])return -1;
    if(ace_handoff_word(record+32)!=UINT64_C(0x313054414e454341) ||
       ace_handoff_word(record+40)!=1 || ace_handoff_word(record+48)!=5 ||
       ace_handoff_word(record+56)!=(uint64_t)(int64_t)-67 ||
       ace_handoff_word(record+192)!=0)return -1;
    static const char prefix[]="\nACEANDROID1:";
    static const char suffix[]=": pending handoff\n";
    uint8_t packet[sizeof(prefix)-1+16+sizeof(suffix)-1+288];size_t n=0;
    for(unsigned i=0;i<sizeof(prefix)-1;i++)packet[n++]=(uint8_t)prefix[i];
    for(unsigned i=0;i<16;i++)packet[n++]=(uint8_t)token[i];
    for(unsigned i=0;i<sizeof(suffix)-1;i++)packet[n++]=(uint8_t)suffix[i];
    for(unsigned i=0;i<288;i++)packet[n++]=record[i];
    return ace_pstore_ring_append(zone,bytes,packet,n);
}
#endif
