; =====================================================================
;  ZAK ATTACK · pantallas: título, presentación de fase, game over, final
; =====================================================================
LOGO_SCR = TXT+$200          ; 120 bytes del logotipo

; ---------------------------------------------------------------------
;  TÍTULO
; ---------------------------------------------------------------------
title:
        jsr hw_off
        jsr stop_music
        lda #0
        sta phase
        sta paused
        jsr setup_phase
        lda #0
        sta camx
        sta camx+1
        sta drawn
        sta drawn+1
        jsr set_scroll
        jsr fill_cols
        ; logotipo
        ldx #119
@lg:    lda logo_map,x
        sta LOGO_SCR,x
        dex
        bpl @lg
        jsr clear_txt
        lda #$40
        sta tmp+3
        lda #<t_sub
        ldx #>t_sub
        ldy #0
        jsr put_line_c20
        lda #0
        sta tmp+3
        lda #<t_by
        ldx #>t_by
        ldy #40
        jsr put_line_c40
        jsr draw_diff
        jsr build_title_dl
        lda #<dli_t1
        sta dlivec
        lda #>dli_t1
        sta dlivec+1
        lda #<TDL
        sta SDLSTL
        lda #>TDL
        sta SDLSTH
        lda #$E0
        sta CHBAS
        lda #$00
        sta COLOR4
        sta COLOR2
        lda #$2A
        sta COLOR0
        lda #$0E
        sta COLOR1
        lda #$1C
        sta COLOR3
        ; Zak grande en la calle
        lda #1
        sta SIZEP0
        sta SIZEP1
        lda #$0C
        sta PCOLR0
        lda #$44
        sta PCOLR1
        ldy #19
@z:     lda zak_a0,y
        sta PL0+156,y
        lda zak_b0,y
        sta PL1+156,y
        dey
        bpl @z
        lda #112
        sta hpos
        sta hpos+1
        lda #$3E
        sta SDMCTL
.ifdef JUKE
        lda #JUKE
.else
        lda #0
.endif
        ldx #1
        jsr play_song
        lda #0
        sta cseq
        sta ctim
        sta cheat
        lda #$FF
        sta oldstk
        lda #1
        sta oldtrg
        ; esperar a soltar el disparo
@rel:   jsr waitvb
        lda STRIG0
        beq @rel
@w:     jsr waitvb
        ; PULSA FIRE parpadeando
        ldx #39
        lda frame
        and #32
        beq @fon
        lda #0
@clr:   sta TXT+120,x
        dex
        bpl @clr
        bmi @rd
@fon:   lda #0
        sta tmp+3
        lda #<t_fire
        ldx #>t_fire
        ldy #120
        jsr put_line_c40
@rd:    ; palanca: flancos
        lda STICK0
        eor #$0F
        tax
        eor oldstk
        and #$FF
        stx oldstk
        and oldstk              ; bits recién pulsados
        sta tedge
        and #4
        beq @nl
        lda diff
        beq @nl
        dec diff
        jsr diff_changed
@nl:    lda tedge
        and #8
        beq @nr
        lda diff
        cmp #2
        bcs @nr
        inc diff
        jsr diff_changed
@nr:    ; truco: abajo, abajo, FIRE (con 2 segundos entre pulsaciones)
        lda ctim
        beq @nt
        dec ctim
        bne @nt
        lda #0
        sta cseq
@nt:    lda tedge
        and #2
        beq @nd
        lda cseq
        cmp #2
        bcs @nd
        inc cseq
        lda #120
        sta ctim
@nd:    ; FIRE (flanco)
        lda STRIG0
        eor #1
        tax
        lda oldtrg
        stx oldtrg
        bne @w2
        cpx #1
        bne @w2
        lda cseq
        cmp #2
        bne @go
        lda ctim
        bne @ch
@go:    jmp start_game
@ch:    lda #1
        sta cheat
        lda #5
        jsr play_sfx
        ldx #39
        lda #0
@cl:    sta TXT+80,x
        dex
        bpl @cl
        sta tmp+3
        lda #<t_inv
        ldx #>t_inv
        ldy #80
        jsr put_line_c40
        lda #90
        sta waitcnt
@iw:    jsr waitvb
        dec waitcnt
        bne @iw
        jmp start_game
@w2:    jmp @w

diff_changed:
        lda #2
        jsr play_sfx
draw_diff:
        ldx #39
        lda #0
@c:     sta TXT+80,x
        dex
        bpl @c
        sta tmp+3
        ldx diff
        lda diff_tlo,x
        pha
        lda diff_thi,x
        tax
        pla
        ldy #80
        jmp put_line_c40
diff_tlo: .byte <t_d0,<t_d1,<t_d2
diff_thi: .byte >t_d0,>t_d1,>t_d2
t_d0:   .byte "DIFICULTAD:      FACIL  >",0
t_d1:   .byte "DIFICULTAD:  <  NORMAL  >",0
t_d2:   .byte "DIFICULTAD:  < HARDCORE",0
t_inv:  .byte "** MODO INVENCIBLE **",0

start_game:
        lda #0
        sta SIZEP0
        sta SIZEP1
        sta phase
        sta score
        sta score+1
        sta score+2
        ldx diff
        lda diff_lives,x
        sta lives
        lda diff_hp,x
        sta hp_max
.ifdef CHEAT
        lda #1
        sta cheat
.endif
next_phase:
        jsr phase_intro
        jsr start_phase
        jmp game_loop

t_sub:  .byte "GATO.COMANDO.CAOS.",0
t_by:   .byte "POR TONY Y CLAUDE A.I.",0
t_fire: .byte "PULSA FIRE",0
t_firecol: .byte $0E

build_title_dl:
        ldx #0
        ldy #0
@c:     lda title_dl,y
        sta TDL,x
        inx
        iny
        cpy #title_dl_end-title_dl
        bne @c
        ; filas de escenario 6..17 (12 filas)
        ldy #6
@r:     lda #$44
        sta TDL,x
        inx
        lda rowlo,y
        sta TDL,x
        inx
        lda rowhi,y
        sta TDL,x
        inx
        iny
        cpy #18
        bne @r
        ldy #0
@t:     lda title_dl2,y
        sta TDL,x
        inx
        iny
        cpy #title_dl2_end-title_dl2
        bne @t
        rts
title_dl:
        .byte $70,$70,$70,$F0
        .byte $44,<LOGO_SCR,>LOGO_SCR,$04,$04
        .byte $70
        .byte $46,<TXT,>TXT
        .byte $F0
title_dl_end:
title_dl2:
        .byte $F0
        .byte $42,<(TXT+40),>(TXT+40)
        .byte $70
        .byte $42,<(TXT+80),>(TXT+80)
        .byte $70
        .byte $42,<(TXT+120),>(TXT+120)
        .byte $41,<TDL,>TDL
title_dl2_end:

; DLI 1: logotipo con degradado línea a línea
dli_t1: pha
        txa
        pha
        lda #>logo_chars
        sta WSYNC
        sta CHBASE
        lda #$42
        sta COLPF0
        lda #$0E
        sta COLPF1
        ldx #0
@l:     lda logo_grad,x
        sta WSYNC
        sta COLPF2
        inx
        cpx #24
        bne @l
        lda #$E0
        sta WSYNC
        sta CHBASE
        lda #$2A
        sta COLPF0
        lda #$0E
        sta COLPF1
        lda #$00
        sta COLPF2
        lda #<dli_t2
        sta VDSLST
        lda #>dli_t2
        sta VDSLST+1
        pla
        tax
        pla
        rti
; DLI 2: escenario de la fase 1
dli_t2: pha
        lda dl_ch
        sta WSYNC
        sta CHBASE
        lda dl_pf+1
        sta COLPF0
        lda dl_pf+2
        sta COLPF1
        lda dl_pf+3
        sta COLPF2
        lda dl_pf
        sta COLBK
        lda #<dli_t3
        sta VDSLST
        lda #>dli_t3
        sta VDSLST+1
        pla
        rti
; DLI 3: textos
dli_t3: pha
        lda #$E0
        sta WSYNC
        sta CHBASE
        lda #0
        sta COLBK
        sta COLPF2
        lda #$0C
        sta COLPF1
        pla
        rti

; ---------------------------------------------------------------------
;  pantallas de texto (4 líneas): A grande (modo 7), B media (modo 6),
;  C y D pequeñas (modo 2)
; ---------------------------------------------------------------------
clear_txt:
        lda #0
        tax
@c:     sta TXT,x
        sta TXT+$100,x
        inx
        bne @c
        rts

; A/X = cadena, Y = desplazamiento en TXT; centra en 20 columnas
put_line_c20:
        sta ptr
        stx ptr+1
        lda #20
        bne put_c
put_line_c40:
        sta ptr
        stx ptr+1
        lda #40
put_c:  sta tmp
        sty tmp+1
        ldy #0
@len:   lda (ptr),y
        beq @l
        iny
        bne @len
@l:     sty tmp+2
        lda tmp
        sec
        sbc tmp+2
        lsr
        clc
        adc tmp+1
        clc
        adc #<TXT
        sta ptr2
        lda #>TXT
        adc #0
        sta ptr2+1
        jmp print

text_dl:
        .byte $70,$70,$70,$70,$70,$70,$70,$70,$70
        .byte $47,<TXT,>TXT
        .byte $70,$70
        .byte $46,<(TXT+20),>(TXT+20)
        .byte $70,$70,$70
        .byte $42,<(TXT+40),>(TXT+40)
        .byte $70
        .byte $42,<(TXT+80),>(TXT+80)
        .byte $41,<TDL,>TDL
text_dl_end:

text_screen_on:
        jsr hw_off
        lda #0
        sta SIZEP0
        sta SIZEP1
        sta SIZEP2
        sta SIZEP3
        ldx #text_dl_end-text_dl-1
@c:     lda text_dl,x
        sta TDL,x
        dex
        bpl @c
        lda #<dli_none
        sta dlivec
        lda #>dli_none
        sta dlivec+1
        lda #<TDL
        sta SDLSTL
        lda #>TDL
        sta SDLSTH
        lda #$E0
        sta CHBAS
        lda #0
        sta COLOR4
        sta COLOR2
        lda #$0E
        sta COLOR1
        lda #$22
        sta SDMCTL
        rts
dli_none:
        rti

; espera A cuadros o FIRE (tras soltarlo)
wait_or_fire:
        sta waitcnt
@rel:   jsr waitvb
        dec waitcnt
        beq @x
        lda STRIG0
        beq @rel
@w:     jsr waitvb
        dec waitcnt
        beq @x
        lda STRIG0
        bne @w
@x:     rts

; ---------------------------------------------------------------------
phase_intro:
        jsr clear_txt
        lda #$2A
        sta COLOR0
        lda #$1C
        sta COLOR3
        ; "FASE n"
        ldx #0
@f:     lda t_fase,x
        sta tmp+3
        beq @fe
        jsr a2i
        sta TXT+7,x
        inx
        bne @f
@fe:    lda phase
        clc
        adc #$11
        sta TXT+12
        ; nombre (modo 6, color PF3)
        ldx phase
        lda ph_namelo,x
        sta ptr
        lda ph_namehi,x
        sta ptr+1
        lda #$C0
        sta tmp+3
        ldy #0
@ln:    lda (ptr),y
        beq @lnd
        iny
        bne @ln
@lnd:   sty tmp+2
        lda #20
        sec
        sbc tmp+2
        lsr
        clc
        adc #20
        adc #<TXT
        sta ptr2
        lda #>TXT
        adc #0
        sta ptr2+1
        jsr print
        lda #0
        sta tmp+3
        ldx phase
        lda boss_names_hi,x
        pha
        lda boss_names_lo,x
        tay
        pla
        tax
        tya
        ldy #40
        jsr put_line_c40
        lda #<t_ready
        ldx #>t_ready
        ldy #80
        jsr put_line_c40
        jsr text_screen_on
        lda #180
        jmp wait_or_fire
t_fase: .byte "FASE ",0
t_ready:.byte "PREPARATE, ZAK",0
boss_names_lo: .byte <bn1,<bn2,<bn3,<bn4,<bn5
boss_names_hi: .byte >bn1,>bn2,>bn3,>bn4,>bn5
bn1:    .byte "JEFE: MEKDOZER 1",0
bn2:    .byte "JEFE: METROPLEX III",0
bn3:    .byte "JEFE: CONTROL CENTRAL II",0
bn4:    .byte "JEFE: QUIMERA-9",0
bn5:    .byte "JEFE: RATTUS PRIME",0

; ---------------------------------------------------------------------
phase_clear:
        inc phase
        lda phase
        cmp #NPHASES
        bcc @np
        jmp ending
@np:    jmp next_phase

; ---------------------------------------------------------------------
score_line:
        ; "PUNTOS 000000" en TXT+20 (modo 6)
        ldx #0
@c:     lda t_pts,x
        beq @d
        jsr a2i
        ora #$40
        sta TXT+23,x
        inx
        bne @c
@d:     ldx #0
        ldy #30
@s:     lda score,x
        lsr
        lsr
        lsr
        lsr
        ora #$50
        sta TXT,y
        iny
        lda score,x
        and #$0F
        ora #$50
        sta TXT,y
        iny
        inx
        cpx #3
        bne @s
        rts
t_pts:  .byte "PUNTOS",0

game_over:
        jsr stop_music
        jsr clear_txt
        lda #0
        sta tmp+3
        lda #$44
        sta COLOR0
        lda #<t_gover
        ldx #>t_gover
        ldy #0
        jsr put_line_c20
        jsr score_line
        lda #<t_rata
        ldx #>t_rata
        ldy #40
        jsr put_line_c40
        jsr text_screen_on
        lda #7
        ldx #0
        jsr play_song
        lda #240
        jsr wait_or_fire
        jmp title
t_gover:.byte "GAME OVER",0
t_rata: .byte "INDUSTRIAS RATA CELEBRA SU VICTORIA",0

ending:
        jsr clear_txt
        lda #0
        sta tmp+3
        lda #$1C
        sta COLOR0
        lda #<t_end1
        ldx #>t_end1
        ldy #0
        jsr put_line_c20
        jsr score_line
        lda #<t_end2
        ldx #>t_end2
        ldy #40
        jsr put_line_c40
        lda #<t_end3
        ldx #>t_end3
        ldy #80
        jsr put_line_c40
        jsr text_screen_on
        lda #6
        ldx #0
        jsr play_song
        lda #0
        sta waitcnt+1
        ldx #3
@w:     txa
        pha
        lda #200
        jsr wait_or_fire
        pla
        tax
        dex
        bne @w
        jmp title
t_end1: .byte "MISION CUMPLIDA",0
t_end2: .byte "LA CIUDAD VUELVE A SER DE LOS GATOS",0
t_end3: .byte "GRACIAS POR JUGAR",0
