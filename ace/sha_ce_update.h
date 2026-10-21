/* SPDX-License-Identifier: MIT */
#ifndef ACE_SHA_CE_UPDATE_H
#define ACE_SHA_CE_UPDATE_H
/* Private SHA update adapter. Caller uses unchanged scalar final/padding. */
extern int native_sha_ce_allowed(void);
extern int guarded_ce_blocks(unsigned *,const unsigned char *,unsigned long);
static void private_ce_update(struct ace_sha256 *s,const unsigned char *p,unsigned long n){
 if(!native_sha_ce_allowed()){ace_sha_update(s,p,n);return;}
 s->bytes+=n;
 if(s->used){
  while(n && s->used<64){s->block[s->used++]=*p++;n--;}
  if(s->used==64){if(!native_sha_ce_allowed() || guarded_ce_blocks(s->h,s->block,1))ace_sha_block(s,s->block);s->used=0;}
 }
 unsigned long blocks=n/64;
 if(blocks){if(!native_sha_ce_allowed() || guarded_ce_blocks(s->h,p,blocks))for(unsigned long i=0;i<blocks;i++)ace_sha_block(s,p+64*i);p+=blocks*64;n-=blocks*64;}
 while(n--){s->block[s->used++]=*p++;}
}

#endif
