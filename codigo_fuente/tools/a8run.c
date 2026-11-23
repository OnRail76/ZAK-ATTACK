#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "libatari800.h"
extern int Colours_table[256];
/* a8run file script outdir : headless runner. script commands:
   run N joy trig  | start N | shot name | mem hexaddr len | key N code */
int main(int argc,char**argv){
  char *args[]={"atari800","-xl","-nobasic","-ntsc","-nopatchall",argv[1],NULL};
  if(libatari800_init(6,args)!=1 && 0){}
  FILE*f=fopen(argv[2],"r"); char line[256]; input_template_t in;
  libatari800_clear_input_array(&in);
  while(fgets(line,256,f)){
    char cmd[32]; int a=0,b=0,c=0; char name[128];
    if(sscanf(line,"%31s",cmd)!=1||cmd[0]=='#')continue;
    if(!strcmp(cmd,"run")){sscanf(line,"%*s %d %d %d",&a,&b,&c);
      for(int i=0;i<a;i++){libatari800_clear_input_array(&in);in.joy0=b;in.trig0=c;libatari800_next_frame(&in);} }
    else if(!strcmp(cmd,"start")){sscanf(line,"%*s %d",&a);
      for(int i=0;i<a;i++){libatari800_clear_input_array(&in);in.start=1;in.joy0=15;in.trig0=1;libatari800_next_frame(&in);} }
    else if(!strcmp(cmd,"shot")){sscanf(line,"%*s %127s",name);char p[300];sprintf(p,"%s/%s.raw",argv[3],name);
      FILE*o=fopen(p,"wb");fwrite(libatari800_get_screen_ptr(),1,384*240,o);fclose(o);}
    else if(!strcmp(cmd,"pal")){FILE*o=fopen("pal.bin","wb");for(int i=0;i<256;i++){int c=Colours_table[i];fputc((c>>16)&255,o);fputc((c>>8)&255,o);fputc(c&255,o);}fclose(o);}
    else if(!strcmp(cmd,"mem")){unsigned ad;sscanf(line,"%*s %x %d",&ad,&a);UBYTE*m=libatari800_get_main_memory_ptr();
      printf("%04X:",ad);for(int i=0;i<a;i++)printf(" %02X",m[ad+i]);printf("\n");}
    else if(!strcmp(cmd,"cpu")){emulator_state_t s;libatari800_get_current_state(&s);cpu_state_t*cp=(cpu_state_t*)&s.state[s.tags.cpu];pc_state_t*pc=(pc_state_t*)&s.state[s.tags.pc];printf("PC=%04X A=%02X X=%02X Y=%02X\n",pc->PC,cp->A,cp->X,cp->Y);}
  }
  libatari800_exit();return 0;}
