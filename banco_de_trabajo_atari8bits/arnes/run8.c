/* run8: ejecuta un .xex en atari800 headless con un guion de entrada.
   guion: lineas "in F0 F1 joy trig start"  "shot F nombre.raw"  "mem F addr len nombre.bin"  "end F" */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "libatari800.h"
typedef struct {int t,f0,f1,joy,trig,start,addr,len;char name[128];} Ev;
int main(int argc,char**argv){
  if(argc<3){fprintf(stderr,"uso: run8 juego.xex guion [-pal]\n");return 1;}
  Ev *ev=malloc(sizeof(Ev)*200000);int n=0;FILE*g=fopen(argv[2],"r");char line[256];int endf=600;
  while(fgets(line,256,g)){Ev e={0};char k[16];
    if(sscanf(line,"%15s",k)!=1||k[0]=='#')continue;
    if(!strcmp(k,"in")){e.t=0;sscanf(line,"%*s %d %d %d %d %d",&e.f0,&e.f1,&e.joy,&e.trig,&e.start);}
    else if(!strcmp(k,"shot")){e.t=1;sscanf(line,"%*s %d %127s",&e.f0,e.name);}
    else if(!strcmp(k,"mem")){e.t=2;sscanf(line,"%*s %d %x %d %127s",&e.f0,&e.addr,&e.len,e.name);}
    else if(!strcmp(k,"end")){sscanf(line,"%*s %d",&endf);continue;}
    else continue; ev[n++]=e;}
  char *args[]={"-xl","-ntsc","-nobasic",argc>3?argv[3]:"-ntsc",argv[1],NULL};
  if(!libatari800_init(5,args)){fprintf(stderr,"init fallo: %s\n",libatari800_error_message());return 1;}
  input_template_t in; FILE*wav=getenv("WAV")?fopen(getenv("WAV"),"wb"):NULL;
  for(int f=0;f<endf;f++){
    libatari800_clear_input_array(&in);
    for(int i=0;i<n;i++) if(ev[i].t==0&&f>=ev[i].f0&&f<=ev[i].f1){in.joy0=ev[i].joy;in.trig0=ev[i].trig;in.start=ev[i].start;}
    libatari800_next_frame(&in);
    if(wav) fwrite(libatari800_get_sound_buffer(),1,libatari800_get_sound_buffer_len(),wav);
    for(int i=0;i<n;i++){
      if(ev[i].t==1&&ev[i].f0==f){FILE*o=fopen(ev[i].name,"wb");fwrite(libatari800_get_screen_ptr(),1,384*240,o);fclose(o);}
      if(ev[i].t==2&&ev[i].f0==f){FILE*o=fopen(ev[i].name,"wb");fwrite(libatari800_get_main_memory_ptr()+ev[i].addr,1,ev[i].len,o);fclose(o);}
    }
  }
  if(wav){fclose(wav);fprintf(stderr,"wav %d Hz %d ch %d bytes/sample\n",libatari800_get_sound_frequency(),libatari800_get_num_sound_channels(),libatari800_get_sound_sample_size());}
  libatari800_exit();return 0;}
