#!/bin/sh
# runbot.sh total cada  -> montaje test/m.png
cd "$(dirname "$0")/.."
rm -f test/b*.raw test/b*.png
python3 tools/bot.py $1 $2 test/b > test/bot.txt
./tools/run8 build/zakattack.xex test/bot.txt >/dev/null 2>&1
python3 tools/shot.py test/b*.raw
python3 - <<'P'
import glob
from PIL import Image
fs=sorted(glob.glob('test/b*.png'))
m=Image.new('RGB',(320*5,240*((len(fs)+4)//5)))
for i,f in enumerate(fs): m.paste(Image.open(f).resize((320,240)),((i%5)*320,(i//5)*240))
m.save('test/m.png'); print(len(fs),'capturas')
P
