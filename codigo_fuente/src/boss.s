; =====================================================================
;  ZAK ATTACK · jefes
;  Cuerpo de caracteres con partes (vida propia). Proyectiles = huecos
;  de enemigo con tipos 9..12. QUIMERA-9 es un sprite doble (P2+P3).
; =====================================================================
T_SHOCK = 9
T_ROCK  = 10
T_FIRE  = 11
T_ARM   = 12

        .bss
bstep:  .res 1
bcore:  .res 1              ; 1 = núcleo vulnerable
bfr:    .res 1
qx:     .res 2              ; QUIMERA: x mundo
qy:     .res 1              ; pies
qvy:    .res 1
qsub:   .res 1
qvx:    .res 1
qdir:   .res 1
qgnd:   .res 1
qoy:    .res 1
bdead:  .res 1
bm_t:   .res 8              ; explosiones de muerte del jefe: vida (0 = libre)
bm_x:   .res 8              ; x hardware
bm_y:   .res 8              ; desplazamiento dentro de la franja
bm_k:   .res 1
bm_min: .res 1              ; primera explosión permitida (franja mínima * 2)
bm_l:   .res 1              ; x hardware del borde izquierdo del jefe
        .code

; ---------------------------------------------------------------------
boss_update:
        lda boss_on
        bne @on
        ; ¿llegó la cámara a la arena?
        lda camx+1
        cmp camxmax+1
        bcc @x
        lda camx
        cmp camxmax
        bcc @x
        jmp boss_start
@x:     rts
@on:    lda bflash
        beq @nf
        dec bflash
        bne @nf
        ldx phase
        lda ph_pf2,x
        sta dl_pf+3
@nf:    lda bossst
        cmp #1
        bne @n1
        jmp boss_fight
@n1:    cmp #2
        bne @n2
        jmp boss_dying
@n2:    cmp #3
        bne @n3
        dec btimer
        bne @r
        lda #6
        ldx #0
        jsr play_song
        lda #200
        sta btimer
        lda #4
        sta bossst
@r:     rts
@n3:    cmp #4
        bne @r
        dec btimer
        bne @r
        lda #9
        sta bossst
        rts

boss_start:
        lda #1
        sta boss_on
        sta bossst
        lda #0
        sta bstep
        sta bcore
        sta bdead
        lda #80
        sta btimer
        ; datos del jefe
        ldx phase
        lda ph_bosslo,x
        sta ptr3
        lda ph_bosshi,x
        sta ptr3+1
        ldy #0
        lda (ptr3),y
        sta bkind
        iny
        lda (ptr3),y
        sta bcol
        iny
        lda (ptr3),y
        sta bcol+1
        iny
        lda (ptr3),y
        sta brow
        ldy #6
        lda (ptr3),y
        sta bnp
        ; partes -> absolutas (columna relativa a bcol, guardamos relativa en bp_c)
        ldx #0
        ldy #7
@p:     lda (ptr3),y
        sta bp_c,x
        iny
        lda (ptr3),y
        clc
        adc brow
        sta bp_r,x
        iny
        lda (ptr3),y
        sta bp_w,x
        iny
        lda (ptr3),y
        sta bp_h,x
        iny
        lda (ptr3),y
        jsr scale_hp
        sta bp_hp,x
        iny
        inx
        cpx #4
        bne @p
        ; núcleo vulnerable de entrada si sólo hay una parte o es MEKDOZER 1
        lda bkind
        cmp #1
        beq @v
        lda bnp
        cmp #2
        bcs @nv
@v:     lda #1
        sta bcore
@nv:    ; fuera enemigos normales
        lda #0
        sta e_type
        sta e_type+1
        sta e_type+2
        sta e_type+3
        lda bkind
        cmp #4
        bne @ns
        jsr quim_init
@ns:    lda #5
        ldx #1
        jmp play_song

; ---------------------------------------------------------------------
; A = x en pantalla del borde izquierdo del jefe
boss_left_edge:
        lda bkind
        cmp #4
        bne @c
        lda #200
        rts
@c:     lda bdead
        beq @a
        lda #200
        rts
@a:     lda bcol
        sta tmp
        lda bcol+1
        asl tmp
        rol
        asl tmp
        rol
        sta tmp+1
        lda tmp
        sec
        sbc camx
        rts

; X = parte -> tmp/tmp+1 = x mundo izquierda (col*4)
part_x: lda bp_c,x
        clc
        adc bcol
        sta tmp
        lda bcol+1
        adc #0
        asl tmp
        rol
        asl tmp
        rol
        sta tmp+1
        rts

; ---------------------------------------------------------------------
;  impacto de la bala X (en tmp+3) contra el jefe
boss_hit_test:
        lda bossst
        cmp #1
        beq @f
        rts
@f:     lda bkind
        cmp #4
        bne @parts
        jmp quim_hit
@parts: ldx #3
@l:     lda bp_hp,x
        beq @n
        cpx #0
        bne @tst
        lda bcore
        beq @n
@tst:   stx tmp+2
        jsr part_x
        ldy tmp+3
        lda b_xl,y
        sec
        sbc tmp
        sta tmp
        lda b_xh,y
        sbc tmp+1
        bne @n0
        ldx tmp+2
        lda bp_w,x
        asl
        asl
        cmp tmp
        bcc @n0
        beq @n0
        lda bp_r,x
        asl
        asl
        asl
        sta tmp
        lda b_y,y
        sec
        sbc tmp
        sta tmp
        lda bp_h,x
        asl
        asl
        asl
        cmp tmp
        bcc @n0
        beq @n0
        ; ¡tocado!
        lda #0
        sta b_on,y
        lda #4
        sta bflash
        lda #$0E
        sta dl_pf+3
        dec bp_hp,x
        bne @snd
        jmp part_destroyed
@snd:   lda #6
        jmp play_sfx
@n0:    ldx tmp+2
@n:     dex
        bpl @l
        ; balas que chocan contra el cuerpo sin daño: desaparecen
        rts

; parte X destruida: escombros en su rectángulo
part_destroyed:
        stx tmp+2
        lda #3
        jsr play_sfx
        lda #$10
        jsr add_score
        ldx phase
        lda ph_rubblelo,x
        sta ptr2
        lda ph_rubblehi,x
        sta ptr2+1
        ldy #0
        lda (ptr2),y
        sta vtmp+1              ; código de escombro
        ldx tmp+2
        jsr fill_part
        ldx tmp+2
        bne @side
        ; núcleo: muere el jefe
        lda #2
        sta bossst
        lda #150
        sta btimer
        jsr boom_start
        jsr stop_music
        rts
@side:  ; ¿quedan partes laterales?
        ldx #3
@c:     lda bp_hp,x
        bne @still
        dex
        bne @c
        lda #1
        sta bcore
@still: rts

; rellena el rectángulo de la parte X con el carácter tmp (A)
fill_part:
        lda bp_r,x
        sta ptr3
        lda bp_h,x
        sta ptr3+1
@row:   lda bp_c,x
        clc
        adc bcol
        sta tx
        lda bcol+1
        adc #0
        sta tx+1
        lda bp_w,x
        sta tmp+1
@col:   stx fp_x
        lda ptr3+1
        cmp #1
        beq @rub
        ; fondo: bg + (tx&15)*22 + fila
        lda tx
        and #15
        tax
        lda mul22,x
        clc
        adc bgp
        sta ptr2
        lda bgp+1
        adc mul22h,x
        sta ptr2+1
        ldy ptr3
        lda (ptr2),y
        jmp @put
@rub:   lda vtmp+1
@put:   ldy ptr3
        jsr putchar
        ldx fp_x
        inc tx
        bne @nc
        inc tx+1
@nc:    dec tmp+1
        bne @col
        inc ptr3
        dec ptr3+1
        bne @row
        rts

; ---------------------------------------------------------------------
boss_fight:
        lda bkind
        cmp #4
        bne @c
        jmp quim_fight
@c:     ; núcleo abierto: parpadeo (bit inverso) cada 8 cuadros
        lda bcore
        beq @nb
        lda bkind
        cmp #1
        beq @nb
        lda frame
        and #7
        bne @nb
        jsr core_blink
@nb:    lda bwarn
        beq @nw
        dec bwarn
        jsr warn_tick
        lda bwarn
        bne @rr
        jsr warn_end
        jmp @atk
@nw:    dec btimer
        beq @pick
@rr:    rts
@pick:  inc bstep
        lda #$FF
        sta bwpart
        lda #0
        sta bwpar
        ldx diff
        lda warn_len,x
        sta bwarn
        lda #8
        jsr play_sfx
        jmp pick_warn
@atk:   lda bkind
        cmp #1
        bne @k2
        jmp atk_grunon
@k2:    cmp #2
        bne @k3
        jmp atk_loco
@k3:    cmp #3
        bne @k5
        jmp atk_horno
@k5:    jmp atk_rattus

core_blink:
        ldx #0
; invierte (bit 7) los caracteres de la parte X
part_toggle:
        lda bp_r,x
        sta ptr3
        lda bp_h,x
        sta ptr3+1
@row:   lda bp_c,x
        clc
        adc bcol
        sta tx
        lda bcol+1
        adc #0
        sta tx+1
        lda bp_w,x
        sta tmp+1
@col:   ldy ptr3
        jsr getchar
        eor #$80
        ldy ptr3
        jsr putchar
        inc tx
        bne @nc
        inc tx+1
@nc:    dec tmp+1
        bne @col
        inc ptr3
        dec ptr3+1
        bne @row
        rts

; ---- avisos
warn_tick:
        lda bwarn
        and #3
        bne @x
        ldx bwpart
        bmi @m
        lda bp_hp,x
        beq @m
        jsr part_toggle
        lda bwpar
        eor #1
        sta bwpar
@m:     lda mark_on
        beq @x
        jsr mark_toggle
@x:     rts
warn_end:
        lda bwpar
        beq @m
        ldx bwpart
        bmi @m
        lda bp_hp,x
        beq @m
        jsr part_toggle
@m:     lda #0
        sta bwpar
        lda mark_on
        beq @x
        lda mark_par
        beq @o
        jsr mark_toggle
@o:     lda #0
        sta mark_on
@x:     rts
; marca en el suelo donde caerá el escombro (2 casillas, fila del suelo)
mark_toggle:
        lda mark_par
        eor #1
        sta mark_par
        lda mark_cl
        sta tx
        lda mark_ch
        sta tx+1
        ldx #0
@one:   lda mark_par
        beq @rest
        ldy #GROUNDY/8-1
        jsr getchar
        sta mark_sv,x
        ldy phase
        lda ph_warnch,y
        jmp @put
@rest:  lda mark_sv,x
@put:   ldy #GROUNDY/8-1
        stx mark_x
        jsr putchar
        ldx mark_x
        inc tx
        bne @n
        inc tx+1
@n:     inx
        cpx #2
        bne @one
        rts

; qué parte avisa (y proyectiles que esperan) para el ataque número bstep
pick_warn:
        lda bkind
        cmp #1
        bne @k2
        ; MEKDOZER 1: escombro cada 4 ataques; el resto, disparos de la cabeza
        lda bstep
        and #3
        cmp #3
        bne @g0
        jmp warn_rock
@g0:    ldx #0
        jmp @set
@k2:    ; resto de jefes: piezas laterales 1 y 2 alternas; con el núcleo abierto, sin aviso de pieza
        lda bcore
        bne @none
        jsr side_part
        bmi @none
@set:   stx bwpart
@none:  rts

; X = pieza lateral que toca (1 o 2, la que siga viva); N=1 si no queda ninguna
side_part:
        lda bstep
        and #1
        tax
        inx
        lda bp_hp,x
        bne @ok
        txa
        eor #3
        tax
        lda bp_hp,x
        bne @ok
        ldx #$FF
@ok:    txa
        rts

warn_rock:
        lda px
        sta tmp
        lda px+1
        sta tmp+1
        lda #16
        sta tmp+2
        lda #T_ROCK
        jsr spawn_proj
        bcs @x
        lda bwarn
        sta e_gnd,x
        ; columna de la marca = (px+4)/4 - ... dos casillas bajo el escombro
        lda px
        clc
        adc #2
        sta mark_cl
        lda px+1
        adc #0
        lsr
        ror mark_cl
        lsr
        ror mark_cl
        sta mark_ch
        lda #1
        sta mark_on
        lda #0
        sta mark_par
@x:     rts

; barrido de RATTUS: el brazo aparece quieto y parpadeando a su altura
warn_arm:
        lda bcol
        sta tmp
        lda bcol+1
        asl tmp
        rol
        asl tmp
        rol
        sta tmp+1
        lda tmp
        sec
        sbc #8
        sta tmp
        bcs @s0
        dec tmp+1
@s0:    lda bstep
        and #2
        beq @low
        lda #GROUNDY-12
        bne @s
@low:   lda #GROUNDY
@s:     sta tmp+2
        lda #T_ARM
        jsr spawn_proj
        bcs @x
        lda #0
        sta e_vx,x
        lda bwarn
        sta e_gnd,x
@x:     rts

; disparo apuntado desde la parte X (centro)
fire_from_part:
        lda bcol
        sta tmp
        lda bcol+1
        asl tmp
        rol
        asl tmp
        rol
        sta tmp+1
        lda tmp
        sec
        sbc #4
        sta tmp
        bcs @c
        dec tmp+1
@c:     lda bp_r,x
        asl
        asl
        asl
        clc
        adc #6
        sta tmp+2
        jmp aim_bullet
; ráfaga: dos balas, la segunda un poco más baja (abanico)
fire_burst:
        jsr fire_from_part
        lda tmp+2
        clc
        adc #14
        sta tmp+2
        jmp aim_bullet

; crea proyectil de jefe: A = tipo, tmp/tmp+1 = x, tmp+2 = y (pies)
spawn_proj:
        sta tmp+3
        ldx #0
        lda e_type
        beq @f
        inx
        lda e_type+1
        beq @f
        sec
        rts
@f:     lda tmp+3
        sta e_type,x
        lda tmp
        sta e_xl,x
        lda tmp+1
        sta e_xh,x
        lda tmp+2
        sta e_y,x
        lda #0
        sta e_st,x
        sta e_vy,x
        sta e_ysub,x
        sta e_t,x
        sta e_gnd,x
        lda #1
        sta e_dir,x
        lda #$FE
        sta e_vx,x
        ldy tmp+3
        lda proj_fr-9,y
        sta e_fr,x
        clc
        rts
proj_fr: .byte EF_SHOCK, EF_ROCK, EF_FIRE, EF_ARM

atk_grunon:
        lda #36
        jsr set_btimer
        lda bstep
        and #3
        cmp #3
        bne @aim
        rts                     ; el escombro ya está cayendo (aviso)
@aim:   ldx #0
        lda bp_hp+1
        bne @one
        jmp fire_burst          ; sin pala: ráfagas
@one:   jmp fire_from_part

; METROPLEX III, CONTROL CENTRAL II y RATTUS PRIME: solo disparos
atk_loco:
        lda #30
        ldy #20
        jmp atk_shoot
; CONTROL CENTRAL II: balas rectas a ras de suelo (hay que saltarlas)
atk_horno:
        lda #34
        ldx bcore
        beq @t
        lda #22
@t:     jsr set_btimer
        lda bcol
        sta tmp
        lda bcol+1
        asl tmp
        rol
        asl tmp
        rol
        sta tmp+1
        lda tmp
        sec
        sbc #4
        sta tmp
        bcs @x
        dec tmp+1
@x:     lda #GROUNDY-14             ; a la altura del pecho de Zak
        sta tmp+2
        lda #$FE
        ldy #0
        jsr new_ebullet
        lda bcore
        beq @r
        lda #GROUNDY-6              ; con el núcleo abierto, otra a la altura de las piernas
        sta tmp+2
        lda #$FE
        ldy #0
        jsr new_ebullet
@r:     rts
atk_rattus:                     ; el jefe final dispara más a menudo
        lda #24
        ldy #14
; A = pausa con piezas laterales, Y = pausa con el núcleo abierto
atk_shoot:
        ldx bcore
        beq @s
        tya
@s:     jsr set_btimer
        lda bcore
        bne @core
        jsr side_part
        bmi @core
        jmp fire_burst
@core:  ldx #0
        jmp fire_burst

; A = cuadros -> btimer ajustado a la dificultad
set_btimer:
        ldy diff
        beq @e
        cpy #2
        bne @n
        sta tmp
        lsr
        lsr
        eor #$FF
        sec
        adc tmp                 ; A - A/4
        jmp @n
@e:     sta tmp
        lsr
        clc
        adc tmp                 ; A + A/2
@n:     sta btimer
        rts

; proyectiles del jefe (llamado desde enemy_one para tipos 9..12)
en_proj:
        lda e_gnd,x
        beq @go
        dec e_gnd,x
        beq @rel
        ; esperando: el escombro tiembla, el brazo parpadea
        lda e_type,x
        cmp #T_ROCK
        bne @harm
        lda #EF_ROCK
        sta e_fr,x
        lda frame
        and #1
        beq @sl
        inc e_xl,x
        rts
@sl:    dec e_xl,x
        rts
@harm:  lda frame
        and #4
        beq @hb
        lda #EF_ARM
        bne @hs
@hb:    lda #EF_BLANK
@hs:    sta e_fr,x
        rts
@rel:   lda e_type,x
        cmp #T_ARM
        bne @rr
        lda #$FD
        sta e_vx,x
        lda #4
        jmp play_sfx
@rr:    lda #7
        jmp play_sfx
@go:    lda e_type,x
        cmp #T_SHOCK
        bne @r
        lda #EF_SHOCK
        sta e_fr,x
        jmp move_x
@r:     cmp #T_ROCK
        bne @f
        lda #EF_ROCK
        sta e_fr,x
        lda e_vy,x
        clc
        adc #1
        cmp #6
        bcs @rc
        sta e_vy,x
@rc:    lda e_y,x
        clc
        adc e_vy,x
        sta e_y,x
        cmp #GROUNDY+2
        bcc @rx
        lda #$80
        sta e_st,x
        lda #16
        sta e_t,x
@rx:    rts
@f:     cmp #T_FIRE
        bne @a
        lda #EF_FIRE
        sta e_fr,x
        jsr move_x
        jsr en_gravity
        bcc @fx
        ; rebote
        lda #$D0
        sta e_vy,x
        dec e_y,x
        inc e_t,x
        lda e_t,x
        cmp #3
        bcc @fx
        lda #$80
        sta e_st,x
        lda #16
        sta e_t,x
@fx:    rts
@a:     lda #EF_ARM
        sta e_fr,x
        jmp move_x

; ---------------------------------------------------------------------
boss_dying:
        dec btimer
        bne @go
        ; borrar el jefe: fondo de la fase en su rectángulo
        jsr boom_end
        jsr erase_boss
        lda #1
        sta bdead
        lda #$01
        jsr add_score_hi
        lda #3
        sta bossst
        lda #60
        sta btimer
        rts
@go:    ; destellos: uno cada 32 cuadros y fogonazo final
        ldx phase
        lda ph_bk,x
        ldy btimer
        cpy #7
        bcs @f1
        lda #$0C
        bne @f2
@f1:    tay
        lda btimer
        and #31
        cmp #2
        tya
        bcs @f2
        ora #$06
@f2:    sta dl_pf
        ; retumbe
        lda btimer
        and #7
        bne @nb
        lda #3
        jsr play_sfx
@nb:    jmp boom_update

; ---------------------------------------------------------------------
;  Explosiones de muerte: 8 a la vez, 2 por franja (4 franjas de la fila 8
;  a la 16, recolocadas por DLI). Cada una nace blanca y acaba roja.
; ---------------------------------------------------------------------
boom_start:
        lda #0
        ldx #7
@c:     sta bm_t,x
        dex
        bpl @c
        sta e_type
        sta e_type+1
        sta e_type+2
        sta e_type+3
        sta b_on+2
        sta b_on+3
        tax
@p:     sta PL2,x
        sta PL3,x
        inx
        bne @p
        ldx bkind
        lda bm_mintab,x
        sta bm_min
        ; borde izquierdo en pantalla (la cámara ya no se mueve)
        cpx #4
        bne @ch
        lda qx
        sec
        sbc camx
        jmp @s
@ch:    lda bcol
        sta tmp
        lda bcol+1
        asl tmp
        rol
        asl tmp
        lda tmp
        sec
        sbc camx
@s:     clc
        adc #HPOFS-2
        sta bm_l
        lda #1
        sta boomon
        rts
bm_mintab: .byte 0, 2, 0, 0, 4, 0      ; MEKDOZER es más bajo; QUIMERA solo abajo

boom_end:
        lda #0
        sta boomon
        sta hposb
        sta hposb+1
        ldx #71
@c:     sta PL2+BOOMTOP,x
        sta PL3+BOOMTOP,x
        dex
        bpl @c
        ldx phase
        lda ph_bk,x
        sta dl_pf
        rts

boom_update:
        ldx #7
@l:     lda bm_t,x
        beq @sp
        dec bm_t,x
        jmp @n
@sp:    lda btimer
        cmp #30
        bcc @n
        cpx bm_min
        bcc @n
        jsr rand
        and #1
        bne @n
        lda #24
        sta bm_t,x
        jsr rand
        and #31
        clc
        adc bm_l
        sta bm_x,x
        lda #0
        cpx #6
        bcc @y
        jsr rand
        and #7
@y:     sta bm_y,x
@n:     dex
        bpl @l
        rts

; pintado (desde draw_sprites, al principio del cuadro)
draw_booms:
        lda #0
        sta hpos+2
        sta hpos+3
        ldx #71
@c:     sta PL2+BOOMTOP,x
        sta PL3+BOOMTOP,x
        dex
        bpl @c
        ldx #7
@b:     stx bm_k
        lda bm_t,x
        bne @on
        sta bh,x
        jmp @n
@on:    lda #24
        sec
        sbc bm_t,x
        lsr
        lsr
        tay
        lda boom_col,y
        sta bc,x
        lda boom_frl,y
        sta ptr
        lda boom_frh,y
        sta ptr+1
        lda bm_x,x
        sta bh,x
        ; destino: PL2/PL3 + BOOMTOP + franja*16 + y
        txa
        and #1
        tay
        lda pl_hi,y
        sta ptr3+1
        txa
        and #6
        asl
        asl
        asl
        clc
        adc #BOOMTOP
        adc bm_y,x
        sta ptr3
        ldy #15
@d:     lda (ptr),y
        sta (ptr3),y
        dey
        bpl @d
        ldx bm_k
@n:     dex
        bpl @b
        lda bh
        sta hposb
        lda bh+1
        sta hposb+1
        lda bc
        sta ecol+2
        lda bc+1
        sta ecol+3
        rts

boom_col:  .byte $0E, $2E, $2C, $3A, $36, $44      ; blanco, amarillo, naranja, rojo
boom_frl:  .byte <boom_gfx, <(boom_gfx+16), <(boom_gfx+16), <(boom_gfx+16), <(boom_gfx+32), <(boom_gfx+48)
boom_frh:  .byte >boom_gfx, >(boom_gfx+16), >(boom_gfx+16), >(boom_gfx+16), >(boom_gfx+32), >(boom_gfx+48)
boom_gfx:     ; 4 cuadros de 8 x 8 con las líneas dobladas (16 líneas)
        .byte $00,$00,$00,$00,$18,$18,$3C,$3C,$3C,$3C,$18,$18,$00,$00,$00,$00
        .byte $24,$24,$18,$18,$7E,$7E,$FF,$FF,$FF,$FF,$7E,$7E,$18,$18,$24,$24
        .byte $BD,$BD,$66,$66,$C3,$C3,$81,$81,$81,$81,$C3,$C3,$66,$66,$BD,$BD
        .byte $42,$42,$99,$99,$24,$24,$42,$42,$42,$42,$24,$24,$99,$99,$42,$42

add_score_hi:
        sed
        clc
        adc score
        sta score
        cld
        lda #1
        sta hudflag
        rts

erase_boss:
        lda bkind
        cmp #4
        bne @c
        lda #0
        sta hpos+2
        sta hpos+3
        rts
@c:     ldx phase
        lda ph_bosslo,x
        sta ptr3
        lda ph_bosshi,x
        sta ptr3+1
        ldy #4
        lda (ptr3),y
        sta tmp+1               ; ancho
        iny
        lda (ptr3),y
        sta tmp+2               ; alto
        lda bcol
        sta tx
        lda bcol+1
        sta tx+1
@col:   ; columna de fondo: bg + (tx&15)*22
        lda tx
        and #15
        tax
        lda mul22,x
        clc
        adc bgp
        sta ptr3
        lda bgp+1
        adc mul22h,x
        sta ptr3+1
        lda brow
        sta bstep
        lda tmp+2
        sta bfr
@row:   ldy bstep
        lda (ptr3),y
        jsr putchar
        inc bstep
        dec bfr
        bne @row
        inc tx
        bne @n
        inc tx+1
@n:     dec tmp+1
        bne @col
        rts

; =====================================================================
;  QUIMERA-9 (sprite doble, P2 + P3 a doble anchura)
; =====================================================================
quim_init:
        lda camx
        clc
        adc #VIS0+108
        sta qx
        lda camx+1
        adc #0
        sta qx+1
        lda #GROUNDY
        sta qy
        lda #0
        sta qvy
        sta qsub
        sta qvx
        sta bfr
        lda #1
        sta qdir
        sta qgnd
        lda #60
        sta btimer
        lda #1
        sta SIZEP2
        sta SIZEP3
        lda #$C6
        sta PCOLR2
        lda #$0C
        sta PCOLR3
        rts

quim_fight:
        lda qgnd
        beq @air
        lda #0
        sta bfr
        ; aviso: parpadea antes de saltar
        ldx diff
        lda warn_half,x
        sta tmp
        lda #$C6
        ldy btimer
        cpy tmp
        bcs @nf
        lda frame
        and #4
        beq @f1
        lda #$0E
        bne @nf
@f1:    lda #$C6
@nf:    sta PCOLR2
        dec btimer
        bne @x
        ; salto: hacia el lado contrario de donde está
        jsr rand
        and #31
        adc #40
        sta btimer
        lda #$B0
        sta qvy
        lda #0
        sta qgnd
        lda #1
        sta bfr
        lda #2
        jsr play_sfx
        ; dirección hacia Zak
        lda qx
        sec
        sbc px
        lda qx+1
        sbc px+1
        lda #$FE
        ldy #1
        bcs @l
        lda #2
        ldy #0
@l:     sta qvx
        sty qdir
@x:     rts
@air:   ; x
        lda qvx
        clc
        adc qx
        sta qx
        lda qvx
        bmi @n
        lda qx+1
        adc #0
        jmp @s
@n:     lda qx+1
        adc #$FF
@s:     sta qx+1
        ; límites de la arena
        lda qx
        sec
        sbc camx
        cmp #VIS0+8
        bcs @l1
        lda #2
        sta qvx
@l1:    cmp #VIS0+124
        bcc @l2
        lda #$FE
        sta qvx
@l2:    ; y
        lda qvy
        clc
        adc #4
        sta qvy
        asl
        asl
        asl
        asl
        clc
        adc qsub
        sta qsub
        lda qvy
        php
        lsr
        lsr
        lsr
        lsr
        plp
        bpl @p
        ora #$F0
@p:     adc qy
        sta qy
        lda qvy
        bmi @r
        ; aterriza en el suelo o en la repisa (fila 11)
        lda qy
        cmp #GROUNDY
        bcc @shelf
        lda #GROUNDY
        bne @land
@shelf: cmp #88
        bcc @r
        cmp #96
        bcs @r
        lda qvy
        cmp #$20
        bcc @r
        lda #88
@land:  sta qy
        lda #1
        sta qgnd
        lda #0
        sta qvy
        lda #3
        jsr play_sfx
        ; dos misiles apuntados al aterrizar
        lda qx
        clc
        adc #16
        sta tmp
        lda qx+1
        adc #0
        sta tmp+1
        lda qy
        sec
        sbc #20
        sta tmp+2
        jsr aim_bullet
        lda qy
        sec
        sbc #12
        sta tmp+2
        jsr aim_bullet
@r:     rts

quim_hit:
        ldy tmp+3
        lda b_xl,y
        sec
        sbc qx
        sta tmp
        lda b_xh,y
        sbc qx+1
        bne @n
        lda tmp
        cmp #32
        bcs @n
        lda qy
        sec
        sbc #22
        sta tmp
        lda b_y,y
        sec
        sbc tmp
        cmp #22
        bcs @n
        lda #0
        sta b_on,y
        lda #4
        sta bflash
        lda #$0E
        sta PCOLR3
        dec bp_hp
        bne @s
        lda #2
        sta bossst
        lda #150
        sta btimer
        jsr boom_start
        jsr stop_music
        lda #0
        sta hpos+2
        sta hpos+3
        sta SIZEP2
        sta SIZEP3
        lda #$1E
        sta PCOLR2
        sta PCOLR3
        jsr clear_p23
@s:     lda #6
        jmp play_sfx
@n:     rts

boss_touch:
        lda bkind
        cmp #4
        bne @x
        lda bossst
        cmp #1
        bne @x
        lda qx
        clc
        adc #2
        sec
        sbc px
        sta tmp
        lda qx+1
        adc #0
        sbc px+1
        bne @x
        ; |Zak dentro del ancho| aproximado: px en [qx-6, qx+26)
        lda tmp
        clc
        adc #6
        cmp #30
        bcs @x
        lda qy
        sec
        sbc #20
        cmp py
        bcs @x
        jsr hurt_player
@x:     rts

boss_draw_sprites:
        lda bkind
        cmp #4
        beq @q
        rts
@q:     lda bflash
        bne @nf
        lda #$0C
        sta PCOLR3
@nf:    ; borrar
        lda #0
        ldy qoy
        ldx #24
@c:     sta PL2,y
        sta PL3,y
        iny
        dex
        bne @c
        lda bossst
        cmp #1
        bne @hide
        lda qy
        clc
        adc #PFTOP-24
        sta qoy
        lda bfr
        beq @f0
        lda #24
@f0:    sta tmp
        ldy qdir
        lda q0lo,y
        clc
        adc tmp
        sta ptr
        lda q0hi,y
        adc #0
        sta ptr+1
        lda q1lo,y
        clc
        adc tmp
        sta ptr2
        lda q1hi,y
        adc #0
        sta ptr2+1
        lda #<PL2
        clc
        adc qoy
        sta ptr3
        lda #>PL2
        sta ptr3+1
        ldy #0
@d:     lda (ptr),y
        sta (ptr3),y
        inc ptr3+1
        lda (ptr2),y
        sta (ptr3),y
        dec ptr3+1
        iny
        cpy #24
        bne @d
        lda qx
        sec
        sbc camx
        clc
        adc #HPOFS
        sta hpos+2
        clc
        adc #16
        sta hpos+3
        rts
@hide:  lda #0
        sta hpos+2
        sta hpos+3
        rts
q0lo:   .byte <quim_0r,<quim_0l
q0hi:   .byte >quim_0r,>quim_0l
q1lo:   .byte <quim_1r,<quim_1l
q1hi:   .byte >quim_1r,>quim_1l

clear_p23:
        lda #0
        tax
@c:     sta PL2,x
        sta PL3,x
        inx
        bne @c
        rts

; A = vida -> ajustada: fácil -25 %, difícil +25 %
scale_hp:
        sty sh_y
        jsr @do
        ldy sh_y
        rts
@do:    ldy diff
        cpy #1
        beq @x
        sta tmp+2
        lsr
        lsr
        sta tmp+3
        lda tmp+2
        cpy #0
        bne @h
        sec
        sbc tmp+3
        rts
@h:     clc
        adc tmp+3
@x:     rts
warn_half: .byte 30,20,12
        .bss
sh_y:   .res 1
fp_x:   .res 1
        .code
