#include "probe-diag.h"
extern int probe_fingerprint_call(uint64_t *,const unsigned char *,unsigned long,unsigned);
/* Required by the unchanged guarded CE routine; never called in this probe test. */
void ce_worker(void){__asm__ volatile("brk #0");}
static void say(const char *s){register unsigned long a __asm__("x0")=4,b __asm__("x1")=(unsigned long)s;__asm__ volatile("hlt #0xf000":"+r"(a),"+r"(b)::"memory");}
static uint64_t cpacr(void){uint64_t x;__asm__ volatile("mrs %0,CPACR_EL1":"=r"(x));return x;}
static int check(uint64_t *o,int rc,uint64_t cp){
#ifdef FIXTURE_EL
 return rc==-1 && o[0]==8 && o[1]==UINT64_MAX && o[2]==UINT64_MAX && o[3]==UINT64_MAX && cpacr()==cp;
#else
 uint64_t d;__asm__ volatile("mrs %0,DAIF":"=r"(d));
 if(o[0]!=4 || o[1]!=d || cpacr()!=cp)return 0;
 if((d&0x3c0)!=0x3c0)return rc==-2 && o[2]==UINT64_MAX && o[3]==UINT64_MAX;
#ifdef FIXTURE_SHA
 #ifdef FIXTURE_UNKNOWN
 return rc==-3 && o[2]==(3UL<<12) && o[3]==UINT64_MAX;
#else
 return rc==-3 && o[2]==0 && o[3]==UINT64_MAX;
#endif
#else
 uint64_t i;__asm__ volatile("mrs %0,ID_AA64ISAR0_EL1":"=r"(i));return rc==0 && o[2]==i && o[3]==cp;
#endif
#endif
}
int test_main(void){
 uint64_t o[4],cp=cpacr();
 for(unsigned i=0;i<4;i++)o[i]=0;
 int rc=native_sha_ce_probe_diag(o);
 if(!check(o,rc,cp)){say("NORMAL_FIELDS_FAIL\n");return 1;}
 /* Exact production DAIF refusal and untouched later sentinels. */
 __asm__ volatile("msr DAIFClr,#2;isb":::"memory");
 rc=native_sha_ce_probe_diag(o);
 if(!check(o,rc,cp)){say("DAIF_REFUSAL_FAIL\n");return 1;}
 __asm__ volatile("msr DAIFSet,#2;isb":::"memory");
 for(unsigned mode=0;mode<2;mode++)if(probe_fingerprint_call(o,0,0,mode)){say("PROBE_STATE_FINGERPRINT_FAIL\n");return 1;}
 say("PROBE_DIAG_FIELDS_SENTINELS_DAIF_Q0_Q31_FPCR_FPSR_CPACR_VBAR_PASS\n");return 0;
}
