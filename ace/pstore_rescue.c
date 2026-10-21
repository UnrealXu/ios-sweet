/* SPDX-License-Identifier: MIT */
#include "pstore_rescue.h"
static uint8_t byte(const uint8_t *zone,const struct ace_pstore_ring_info *r,size_t i) {
    size_t first=r->size==r->capacity?r->start:0;
    return zone[12+(first+i)%r->capacity];
}
static int match(const uint8_t *zone,const struct ace_pstore_ring_info *r,
                 size_t at,const char *text,size_t n) {
    if(at>r->size || n>r->size-at)return 0;
    for(size_t i=0;i<n;i++)if(byte(zone,r,at+i)!=(uint8_t)text[i])return 0;
    return 1;
}
static uint64_t word(const uint8_t *p) {
    uint64_t v=0;for(unsigned i=0;i<8;i++)v|=(uint64_t)p[i]<<(8*i);return v;
}
static int envelope(const uint8_t *p,const char token[17],int rescue) {
    static const char magic[]="ACEFALL1";
    for(unsigned i=0;i<8;i++)if(p[i]!=(uint8_t)magic[i])return 0;
    for(unsigned i=0;i<17;i++)if(p[8+i]!=(uint8_t)token[i])return 0;
    for(unsigned i=25;i<32;i++)if(p[i])return 0;
    return word(p+32)==UINT64_C(0x313054414e454341) && word(p+40)==1 &&
        word(p+48)==5 && word(p+56)==(uint64_t)(int64_t)-67 && word(p+192)==0 &&
        word(p+280)==(rescue?ACE_RAM_RESCUE_WORD:0);
}
int ace_pstore_ram_attempt(const void *zone,size_t bytes,const char token[17]) {
    int rc=ace_pstore_trial_pending(zone,bytes,token);
    if(rc!=1)return rc<0?rc:ACE_PSTORE_RING_E_STATE;
    struct ace_pstore_ring_info r;rc=ace_pstore_ring_validate(zone,bytes,&r);if(rc)return rc;
    char armed[]="\nACETRIAL1:0000000000000000: armed\n";
    char handoff[]="\nACEANDROID1:0000000000000000: pending handoff\n";
    char rescue[]="\nACERESCUE1:0000000000000000: selected\n";
    for(unsigned i=0;i<16;i++) {armed[11+i]=token[i];handoff[13+i]=token[i];rescue[12+i]=token[i];}
    unsigned armed_count=0,normal_count=0,rescue_count=0;const uint8_t *p=zone;
    for(size_t i=0;i<r.size;i++) {
        if(match(p,&r,i,armed,sizeof(armed)-1)) {
            if(++armed_count!=1 || normal_count || rescue_count)return ACE_PSTORE_RING_E_STATE;
        }
        size_t remaining=r.size-i;
        if((remaining>=13 && remaining<sizeof(handoff)-1 && match(p,&r,i,handoff,remaining)) ||
           (remaining>=12 && remaining<sizeof(rescue)-1 && match(p,&r,i,rescue,remaining)) ||
           (remaining>=11 && remaining<sizeof(armed)-1 && match(p,&r,i,armed,remaining)))
            return ACE_PSTORE_RING_E_STATE;
        int kind=match(p,&r,i,handoff,sizeof(handoff)-1)?1:
                 match(p,&r,i,rescue,sizeof(rescue)-1)?2:0;
        if(!kind)continue;
        size_t length=kind==1?sizeof(handoff)-1:sizeof(rescue)-1;
        if(armed_count!=1 || 288>r.size-i-length)return ACE_PSTORE_RING_E_STATE;
        uint8_t record[288];for(unsigned j=0;j<288;j++)record[j]=byte(p,&r,i+length+j);
        if(!envelope(record,token,kind==2))return ACE_PSTORE_RING_E_STATE;
        if(kind==1) {
            if(++normal_count!=1 || rescue_count)return ACE_PSTORE_RING_E_STATE;
        } else if(normal_count!=1 || ++rescue_count!=1)return ACE_PSTORE_RING_E_STATE;
        i+=length+288-1; /* opaque record bytes cannot create nested markers */
    }
    return rescue_count?ACE_RAM_STOP:normal_count?ACE_RAM_RESCUE:ACE_RAM_FIRST;
}
int ace_pstore_rescue_selected(void *zone,size_t bytes,const char token[17],
    const uint8_t *record,size_t length) {
    if(!record || length!=288)return ACE_PSTORE_RING_E_ARGUMENT;
    int stage=ace_pstore_ram_attempt(zone,bytes,token);
    if(stage!=ACE_RAM_RESCUE)return stage<0?stage:ACE_PSTORE_RING_E_STATE;
    if(!envelope(record,token,1))return ACE_PSTORE_RING_E_ARGUMENT;
    char marker[]="\nACERESCUE1:0000000000000000: selected\n";
    for(unsigned i=0;i<16;i++)marker[12+i]=token[i];
    uint8_t packet[sizeof(marker)-1+288];
    for(unsigned i=0;i<sizeof(marker)-1;i++)packet[i]=(uint8_t)marker[i];
    for(unsigned i=0;i<288;i++)packet[sizeof(marker)-1+i]=record[i];
    return ace_pstore_ring_append(zone,bytes,packet,sizeof(packet));
}
