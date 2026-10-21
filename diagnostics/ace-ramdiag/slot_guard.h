/* Bounded text parsing before any stock init or policy setup. No libc. */
#ifndef ACE_RAMDIAG_SLOT_GUARD_H
#define ACE_RAMDIAG_SLOT_GUARD_H
static int ace_slot_space(unsigned char c) {
    return c==' ' || c=='\t' || c=='\r' || c=='\n';
}
static int ace_slot_prefix(const unsigned char *p,unsigned long n,const char *key,unsigned long k) {
    if(n<k)return 0;
    for(unsigned long i=0;i<k;i++)if(p[i]!=(unsigned char)key[i])return 0;
    return 1;
}
static int ace_slot_value(const unsigned char *p,unsigned long n) {
    while(n && ace_slot_space(*p)){p++;n--;}
    while(n && ace_slot_space(p[n-1]))n--;
    return (n==2 && p[0]=='_' && p[1]=='b') ||
           (n==4 && p[0]=='"' && p[1]=='_' && p[2]=='b' && p[3]=='"');
}
/* 0 absent, 1 all values B, -1 any malformed/different value. */
static int ace_slot_cmdline(const unsigned char *p,unsigned long n) {
    const char key[]="androidboot.slot_suffix=";int found=0;
    for(unsigned long at=0;at<n;) {
        while(at<n && ace_slot_space(p[at]))at++;
        unsigned long end=at;while(end<n && !ace_slot_space(p[end]))end++;
        if(ace_slot_prefix(p+at,end-at,key,sizeof(key)-1)) {
            if(!ace_slot_value(p+at+sizeof(key)-1,end-at-(sizeof(key)-1)))return -1;
            found=1;
        }
        at=end;
    }
    return found;
}
static int ace_slot_bootconfig(const unsigned char *p,unsigned long n) {
    const char key[]="androidboot.slot_suffix";int found=0;
    for(unsigned long at=0;at<n;) {
        unsigned long end=at;while(end<n && p[end]!='\n')end++;
        unsigned long start=at;while(start<end && ace_slot_space(p[start]))start++;
        if(ace_slot_prefix(p+start,end-start,key,sizeof(key)-1)) {
            unsigned long value=start+sizeof(key)-1;
            if(value==end)return -1;
            if(value<end && (ace_slot_space(p[value]) || p[value]=='=')) {
                while(value<end && ace_slot_space(p[value]))value++;
                if(value==end || p[value]!='=')return -1;
                value++;while(value<end && ace_slot_space(p[value]))value++;
                if(!ace_slot_value(p+value,end-value))return -1;
                found=1;
            }
        }
        at=end<n?end+1:end;
    }
    return found;
}
static int ace_slot_states_valid(int cmdline,int bootconfig) {
    return cmdline>=0 && bootconfig>=0 && (cmdline==1 || bootconfig==1);
}
#endif
