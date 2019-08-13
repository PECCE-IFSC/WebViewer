!/bin/bash
xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --start-fullscreen https://pacheco.tk http://sites.florianopolis.ifsc.edu.br/pecce/ http://www.florianopolis.ifsc.edu.br/ &

sleep 60
xdotool keydown Return
xdotool keyup Return

while true; do
   xdotool keydown ctrl+Tab; xdotool keyup ctrl+Tab;
   sleep 20
done
