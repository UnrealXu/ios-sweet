/* SPDX-License-Identifier: MIT; generated from the separately reviewed private intrinsic core. */
	.arch armv8-a+crypto
	.file	"ce-core.c"
	.text
	.align	2
	.p2align 4,,15
	.global	ce_blocks
	.type	ce_blocks, %function
ce_blocks:
.LFB3900:
	.cfi_startproc
	ldp	q2, q1, [x0]
	cbz	x2, .L9
	sub	x3, x2, #1
	adrp	x2, .LC0
	ldr	q26, [x2, #:lo12:.LC0]
	adrp	x2, .LC1
	ldr	q25, [x2, #:lo12:.LC1]
	adrp	x2, .LC2
	ldr	q24, [x2, #:lo12:.LC2]
	adrp	x2, .LC3
	ldr	q23, [x2, #:lo12:.LC3]
	adrp	x2, .LC4
	ldr	q22, [x2, #:lo12:.LC4]
	adrp	x2, .LC5
	ldr	q21, [x2, #:lo12:.LC5]
	adrp	x2, .LC6
	ldr	q20, [x2, #:lo12:.LC6]
	adrp	x2, .LC7
	ldr	q19, [x2, #:lo12:.LC7]
	adrp	x2, .LC8
	ldr	q18, [x2, #:lo12:.LC8]
	adrp	x2, .LC9
	ldr	q17, [x2, #:lo12:.LC9]
	adrp	x2, .LC10
	ldr	q16, [x2, #:lo12:.LC10]
	adrp	x2, .LC11
	ldr	q7, [x2, #:lo12:.LC11]
	adrp	x2, .LC12
	ldr	q6, [x2, #:lo12:.LC12]
	adrp	x2, .LC13
	ldr	q5, [x2, #:lo12:.LC13]
	adrp	x2, .LC14
	ldr	q4, [x2, #:lo12:.LC14]
	adrp	x2, .LC15
	ldr	q3, [x2, #:lo12:.LC15]
	stp	d8, d9, [sp, -32]!
	.cfi_def_cfa_offset 32
	.cfi_offset 72, -32
	.cfi_offset 73, -24
	str	d10, [sp, 16]
	.cfi_offset 74, -16
	.p2align 3,,7
.L3:
	ldp	q30, q29, [x1]
	sub	x3, x3, #1
	mov	v8.16b, v2.16b
	cmn	x3, #1
	mov	v0.16b, v1.16b
	rev32	v30.16b, v30.16b
	rev32	v29.16b, v29.16b
	ldp	q28, q27, [x1, 32]
	add	x1, x1, 64
	add	v9.4s, v26.4s, v30.4s
	add	v31.4s, v25.4s, v29.4s
	rev32	v28.16b, v28.16b
	rev32	v27.16b, v27.16b
	sha256h	q8, q1, v9.4s
	sha256h2	q0, q2, v9.4s
	add	v9.4s, v24.4s, v28.4s
	sha256su0	v30.4s, v29.4s
	sha256su0	v29.4s, v28.4s
	mov	v10.16b, v8.16b
	sha256su1	v30.4s, v28.4s, v27.4s
	sha256su0	v28.4s, v27.4s
	sha256h	q10, q0, v31.4s
	sha256h2	q0, q8, v31.4s
	add	v8.4s, v23.4s, v27.4s
	sha256su1	v29.4s, v27.4s, v30.4s
	sha256su0	v27.4s, v30.4s
	mov	v31.16b, v10.16b
	sha256su1	v28.4s, v30.4s, v29.4s
	sha256h	q31, q0, v9.4s
	sha256h2	q0, q10, v9.4s
	add	v10.4s, v30.4s, v22.4s
	sha256su0	v30.4s, v29.4s
	sha256su1	v27.4s, v29.4s, v28.4s
	mov	v9.16b, v31.16b
	sha256h	q9, q0, v8.4s
	sha256h2	q0, q31, v8.4s
	add	v31.4s, v29.4s, v21.4s
	sha256su1	v30.4s, v28.4s, v27.4s
	sha256su0	v29.4s, v28.4s
	mov	v8.16b, v9.16b
	sha256su1	v29.4s, v27.4s, v30.4s
	sha256h	q8, q0, v10.4s
	sha256h2	q0, q9, v10.4s
	add	v10.4s, v28.4s, v20.4s
	sha256su0	v28.4s, v27.4s
	mov	v9.16b, v8.16b
	sha256su1	v28.4s, v30.4s, v29.4s
	sha256h	q9, q0, v31.4s
	sha256h2	q0, q8, v31.4s
	add	v31.4s, v27.4s, v19.4s
	sha256su0	v27.4s, v30.4s
	mov	v8.16b, v9.16b
	sha256su1	v27.4s, v29.4s, v28.4s
	sha256h	q8, q0, v10.4s
	sha256h2	q0, q9, v10.4s
	add	v10.4s, v30.4s, v18.4s
	sha256su0	v30.4s, v29.4s
	mov	v9.16b, v8.16b
	sha256su1	v30.4s, v28.4s, v27.4s
	sha256h	q9, q0, v31.4s
	sha256h2	q0, q8, v31.4s
	add	v31.4s, v29.4s, v17.4s
	sha256su0	v29.4s, v28.4s
	mov	v8.16b, v9.16b
	sha256su1	v29.4s, v27.4s, v30.4s
	sha256h	q8, q0, v10.4s
	sha256h2	q0, q9, v10.4s
	add	v10.4s, v28.4s, v16.4s
	sha256su0	v28.4s, v27.4s
	mov	v9.16b, v8.16b
	sha256su1	v28.4s, v30.4s, v29.4s
	sha256h	q9, q0, v31.4s
	sha256h2	q0, q8, v31.4s
	add	v31.4s, v27.4s, v7.4s
	sha256su0	v27.4s, v30.4s
	mov	v8.16b, v9.16b
	sha256su1	v27.4s, v29.4s, v28.4s
	add	v28.4s, v28.4s, v4.4s
	sha256h	q8, q0, v10.4s
	sha256h2	q0, q9, v10.4s
	add	v10.4s, v30.4s, v6.4s
	add	v27.4s, v27.4s, v3.4s
	mov	v9.16b, v8.16b
	sha256h	q9, q0, v31.4s
	sha256h2	q0, q8, v31.4s
	add	v8.4s, v29.4s, v5.4s
	mov	v31.16b, v9.16b
	sha256h	q31, q0, v10.4s
	sha256h2	q0, q9, v10.4s
	mov	v30.16b, v31.16b
	sha256h	q30, q0, v8.4s
	sha256h2	q0, q31, v8.4s
	mov	v29.16b, v30.16b
	sha256h	q29, q0, v28.4s
	sha256h2	q0, q30, v28.4s
	mov	v8.16b, v29.16b
	sha256h	q8, q0, v27.4s
	sha256h2	q0, q29, v27.4s
	add	v2.4s, v2.4s, v8.4s
	add	v1.4s, v1.4s, v0.4s
	bne	.L3
	ldr	d10, [sp, 16]
	ldp	d8, d9, [sp], 32
	.cfi_restore 73
	.cfi_restore 72
	.cfi_restore 74
	.cfi_def_cfa_offset 0
	stp	q2, q1, [x0]
	ret
.L9:
	stp	q2, q1, [x0]
	ret
	.cfi_endproc
.LFE3900:
	.size	ce_blocks, .-ce_blocks
	.section	.rodata.cst16,"aM",@progbits,16
	.align	4
.LC0:
	.word	1116352408
	.word	1899447441
	.word	-1245643825
	.word	-373957723
	.align	4
.LC1:
	.word	961987163
	.word	1508970993
	.word	-1841331548
	.word	-1424204075
	.align	4
.LC2:
	.word	-670586216
	.word	310598401
	.word	607225278
	.word	1426881987
	.align	4
.LC3:
	.word	1925078388
	.word	-2132889090
	.word	-1680079193
	.word	-1046744716
	.align	4
.LC4:
	.word	-459576895
	.word	-272742522
	.word	264347078
	.word	604807628
	.align	4
.LC5:
	.word	770255983
	.word	1249150122
	.word	1555081692
	.word	1996064986
	.align	4
.LC6:
	.word	-1740746414
	.word	-1473132947
	.word	-1341970488
	.word	-1084653625
	.align	4
.LC7:
	.word	-958395405
	.word	-710438585
	.word	113926993
	.word	338241895
	.align	4
.LC8:
	.word	666307205
	.word	773529912
	.word	1294757372
	.word	1396182291
	.align	4
.LC9:
	.word	1695183700
	.word	1986661051
	.word	-2117940946
	.word	-1838011259
	.align	4
.LC10:
	.word	-1564481375
	.word	-1474664885
	.word	-1035236496
	.word	-949202525
	.align	4
.LC11:
	.word	-778901479
	.word	-694614492
	.word	-200395387
	.word	275423344
	.align	4
.LC12:
	.word	430227734
	.word	506948616
	.word	659060556
	.word	883997877
	.align	4
.LC13:
	.word	958139571
	.word	1322822218
	.word	1537002063
	.word	1747873779
	.align	4
.LC14:
	.word	1955562222
	.word	2024104815
	.word	-2067236844
	.word	-1933114872
	.align	4
.LC15:
	.word	-1866530822
	.word	-1538233109
	.word	-1090935817
	.word	-965641998
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
