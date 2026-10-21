/* Host QEMU fixture only. Fixed addresses below are simulator RAM, not Ace. */
#include "../xnu_handoff.h"
extern const uint8_t bundle_start[],bundle_end[],_start[],image_end[];
extern volatile uint64_t harness_record[4];
extern void handoff_jump(uint64_t entry,uint64_t args) __attribute__((noreturn));
#define RAM 0x41000000UL
#define SIZE 0x40000UL
void loader_main(void) {
    /* Exclusive QEMU RAM deliberately outside the loader and source image. */
    volatile uint8_t *ram=(void *)RAM;
    for(unsigned i=0;i<SIZE;i++) ram[i]=0xa5;
    struct ace_xnu_range reserved={(uintptr_t)_start,(uintptr_t)image_end-(uintptr_t)_start};
    struct ace_xnu_policy policy={.ram={RAM,SIZE},
        .source={(uintptr_t)bundle_start,(uintptr_t)bundle_end-(uintptr_t)bundle_start},
        .reserved=&reserved,.reserved_count=1};
    struct ace_xnu_plan plan;
    int rc=ace_xnu_materialize(bundle_start,policy.source.size,&policy,(void *)RAM,SIZE,&plan);
    harness_record[0]=rc?2:1;harness_record[1]=(uint64_t)(int64_t)rc;
    if(rc) return;
    harness_record[2]=plan.entry_pa;harness_record[3]=plan.args_pa;
    handoff_jump(plan.entry_pa,plan.args_pa);
}
