; =====================================================================
;  Vórtice 5 · cargador de cartucho AtariMax 128 KB (banco 0)
;  Copia los bancos 1-4 a RAM $2000-$9FFF, desactiva el cartucho
;  (queda RAM en $A000-$BFFF) y arranca el juego en $2000.
; =====================================================================
        .segment "CART"
        .org $A000
cstart:
        ldx #reloc_end-reloc-1
@c:     lda reloc_src,x
        sta $0600,x
        dex
        bpl @c
        jmp $0600
cinit:  rts
reloc_src:
        .org $0600
reloc:
        sei
        lda #1
        sta $CF                 ; banco
@b:     ldx $CF
        sta $D500,x             ; selecciona banco
        lda #0
        sta $CB
        sta $CD
        lda #$A0
        sta $CC
        lda $CF
        asl
        asl
        asl
        asl
        asl                     ; banco*32
        sta $CE                 ; destino $2000,$4000,$6000,$8000
        ldx #32
        ldy #0
@p:     lda ($CB),y
        sta ($CD),y
        iny
        bne @p
        inc $CC
        inc $CE
        dex
        bne @p
        inc $CF
        lda $CF
        cmp #5
        bne @b
        sta $D510               ; cartucho fuera
        cli
        jmp $2000
reloc_end:
        .reloc
        .segment "VEC"
        .word cstart
        .byte 0
        .byte $04
        .word cinit
