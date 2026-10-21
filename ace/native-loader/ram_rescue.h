/* SPDX-License-Identifier: MIT */
#ifndef ACE_NATIVE_RAM_RESCUE_H
#define ACE_NATIVE_RAM_RESCUE_H
#include "../fdt.h"
struct native_rescue_plan { uint64_t start,end,new_end; int state; uint8_t capability[24]; };
int native_ram_rescue_prepare(const struct ace_fdt *,uint64_t,struct native_rescue_plan *);
int native_ram_rescue_commit(const struct native_rescue_plan *,const uint8_t *,size_t);
void native_ram_rescue_failure_trace(const struct ace_fdt *,char,int);
#endif
