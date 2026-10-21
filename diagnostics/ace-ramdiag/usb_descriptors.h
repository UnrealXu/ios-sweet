/* Bounded parser for the single ADB interface in our dummy_hcd fixture. */
#ifndef ACE_USB_DESCRIPTORS_H
#define ACE_USB_DESCRIPTORS_H
struct ace_usb_endpoints {unsigned in,out,packet;};
static unsigned ace_usb_le16(const unsigned char *p){return p[0]|((unsigned)p[1]<<8);}
static int ace_usb_descriptors(const unsigned char *p,unsigned long n,struct ace_usb_endpoints *ep) {
    if(n<18 || p[0]!=18 || p[1]!=1 || ace_usb_le16(p+8)!=0x18d1 || ace_usb_le16(p+10)!=0xd001 || p[17]!=1)return 0;
    unsigned config=0,interfaces=0,endpoints=0,packet=0;ep->in=0;ep->out=0;
    for(unsigned long at=18;at<n;) {
        if(n-at<2 || p[at]<2 || p[at]>n-at)return 0;
        unsigned size=p[at],type=p[at+1];const unsigned char *d=p+at;
        if(type==2) {
            if(size!=9 || config++ || ace_usb_le16(d+2)!=n-at || d[4]!=1 || d[5]!=1)return 0;
        } else if(type==4) {
            if(!config || size!=9 || interfaces++ || d[2]!=0 || d[3]!=0 || d[4]!=2 || d[5]!=0xff || d[6]!=0x42 || d[7]!=1)return 0;
        } else if(type==5) {
            if(!interfaces || size!=7 || (d[3]&3)!=2 || !(d[2]&15) || (d[2]&0x70))return 0;
            unsigned current=ace_usb_le16(d+4);
            if((current!=64 && current!=512) || (packet && current!=packet))return 0;
            packet=current;
            if(d[2]&0x80){if(ep->in)return 0;ep->in=d[2];}
            else {if(ep->out)return 0;ep->out=d[2];}
            endpoints++;
        } else if(type==9) {if(size!=3 || (d[2]&~3U))return 0;}
        else if(type==0x0b) {if(size!=8 || d[2]!=0 || d[3]!=1)return 0;}
        else if(type==0x30) {if(size!=6)return 0;}
        else return 0;
        at+=size;
    }
    ep->packet=packet;
    return config==1 && interfaces==1 && endpoints==2 && ep->in && ep->out;
}
#endif
