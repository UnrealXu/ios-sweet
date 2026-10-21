/* SPDX-License-Identifier: MIT */
/* RAM rescue only; no higher-EL trap recovery promised. */
.arch armv8-a+crypto
.text
.global guarded_ce_blocks
guarded_ce_blocks:
 mrs x9,CurrentEL
 cmp x9,#4
 b.ne refuse
 mrs x9,ID_AA64ISAR0_EL1
 ubfx x9,x9,#12,#4
 cmp x9,#1
 b.lo refuse
 cmp x9,#2
 b.hi refuse
 mrs x9,DAIF
 and x9,x9,#0x3c0
 cmp x9,#0x3c0
 b.ne refuse
 sub sp,sp,#576
 str x29,[sp,#544]
 str x30,[sp,#552]
 mrs x9,CPACR_EL1
 str x9,[sp,#528]
 orr x10,x9,#(3<<20)
 msr CPACR_EL1,x10
 isb
 stp q0,q1,[sp,#0]
 stp q2,q3,[sp,#32]
 stp q4,q5,[sp,#64]
 stp q6,q7,[sp,#96]
 stp q8,q9,[sp,#128]
 stp q10,q11,[sp,#160]
 stp q12,q13,[sp,#192]
 stp q14,q15,[sp,#224]
 stp q16,q17,[sp,#256]
 stp q18,q19,[sp,#288]
 stp q20,q21,[sp,#320]
 stp q22,q23,[sp,#352]
 stp q24,q25,[sp,#384]
 stp q26,q27,[sp,#416]
 stp q28,q29,[sp,#448]
 stp q30,q31,[sp,#480]
 mrs x9,FPCR
 mrs x10,FPSR
 str x9,[sp,#512]
 str x10,[sp,#520]
 bl ce_worker
 ldr x9,[sp,#512]
 ldr x10,[sp,#520]
 msr FPCR,x9
 msr FPSR,x10
 ldp q0,q1,[sp,#0]
 ldp q2,q3,[sp,#32]
 ldp q4,q5,[sp,#64]
 ldp q6,q7,[sp,#96]
 ldp q8,q9,[sp,#128]
 ldp q10,q11,[sp,#160]
 ldp q12,q13,[sp,#192]
 ldp q14,q15,[sp,#224]
 ldp q16,q17,[sp,#256]
 ldp q18,q19,[sp,#288]
 ldp q20,q21,[sp,#320]
 ldp q22,q23,[sp,#352]
 ldp q24,q25,[sp,#384]
 ldp q26,q27,[sp,#416]
 ldp q28,q29,[sp,#448]
 ldp q30,q31,[sp,#480]
 ldr x9,[sp,#528]
 msr CPACR_EL1,x9
 isb
 ldr x29,[sp,#544]
 ldr x30,[sp,#552]
 add sp,sp,#576
 mov w0,#0
 ret
refuse:
 mov w0,#1
 ret

/* Fresh observations only. Does not enable FP/SIMD or modify sysregs. */
.global native_sha_ce_probe
native_sha_ce_probe:
 mrs x9,CurrentEL
 cmp x9,#4
 b.ne probe_refuse
 mrs x9,DAIF
 and x9,x9,#0x3c0
 cmp x9,#0x3c0
 b.ne probe_refuse
 mrs x9,ID_AA64ISAR0_EL1
 ubfx x10,x9,#12,#4
 cmp x10,#1
 b.lo probe_refuse
 cmp x10,#2
 b.hi probe_refuse
 mrs x10,CPACR_EL1
 stp x9,x10,[x0]
 mov w0,#0
 ret
probe_refuse:
 mov w0,#-1
 ret
.section .note.GNU-stack,"",%progbits
