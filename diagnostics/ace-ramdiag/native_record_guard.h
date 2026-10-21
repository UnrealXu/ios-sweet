/* The current native refusal envelope, never an iOS success marker. */
#ifndef ACE_NATIVE_RECORD_GUARD_H
#define ACE_NATIVE_RECORD_GUARD_H
static unsigned long ace_record_word(const unsigned char *p) {
    unsigned long v=0;for(unsigned i=0;i<8;i++)v|=(unsigned long)p[i]<<(i*8);return v;
}
static int ace_native_refusal_record(const unsigned char *p,unsigned long n,const char *token) {
    if(n!=288)return 0;
    const char magic[]="ACEFALL1";
    for(unsigned i=0;i<8;i++)if(p[i]!=(unsigned char)magic[i] || p[24+i])return 0;
    for(unsigned i=0;i<16;i++) {
        if(!((token[i]>='0' && token[i]<='9') || (token[i]>='a' && token[i]<='f')) || p[8+i]!=(unsigned char)token[i])return 0;
    }
    return !token[16] && ace_record_word(p+32)==0x313054414e454341UL &&
        ace_record_word(p+40)==1 && ace_record_word(p+48)>=1 && ace_record_word(p+48)<=7 &&
        ace_record_word(p+56)>=(unsigned long)-127 && !ace_record_word(p+192);
}
#endif
