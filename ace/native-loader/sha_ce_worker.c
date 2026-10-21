/* SPDX-License-Identifier: MIT */
/* Runs ONLY inside guarded FP/SIMD access epoch; ordinary general-regs C. */
extern void ce_blocks(unsigned *,const unsigned char *,unsigned long);
void ce_worker(unsigned h[8],const unsigned char *p,unsigned long blocks){
 unsigned local[8] __attribute__((aligned(16)));
 unsigned char staging[64] __attribute__((aligned(16)));
 for(unsigned i=0;i<8;i++)local[i]=h[i];
 if(!((unsigned long)p&15))ce_blocks(local,p,blocks);
 else while(blocks--){
  for(unsigned i=0;i<64;i++)staging[i]=p[i];
  ce_blocks(local,staging,1);p+=64;
 }
 for(unsigned i=0;i<8;i++)h[i]=local[i];
}
