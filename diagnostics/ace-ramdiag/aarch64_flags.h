/* Linux ARM64 UAPI, not asm-generic/x86 values. See arch/arm64/include/uapi/
 * asm/fcntl.h; O_DIRECTORY/O_NOFOLLOW are overridden for AArch32 compat. */
#ifndef ACE_AARCH64_FLAGS_H
#define ACE_AARCH64_FLAGS_H
#define ACE_O_DIRECTORY 040000
#define ACE_O_NOFOLLOW 0100000
#define ACE_O_CLOEXEC 02000000
#define ACE_O_PATH 010000000
#endif
