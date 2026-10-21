/* Linux pmsg has a dynamically allocated character major, minor zero.
 * Parse only the complete sysfs dev attribute, never a guessed misc minor. */
#ifndef ACE_PMSG_TRACE_H
#define ACE_PMSG_TRACE_H
static int ace_pmsg_major(const unsigned char *s,unsigned long n) {
    if(!s || n<4 || n>7 || s[0]<'1' || s[0]>'9')return -1;
    unsigned long i=0;unsigned value=0;
    while(i<n && s[i]>='0' && s[i]<='9') {
        value=value*10+s[i++]-'0';if(value>4095)return -1;
    }
    if(n-i!=3 || s[i]!=':' || s[i+1]!='0' || s[i+2]!='\n')return -1;
    return (int)value;
}
#endif
