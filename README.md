# WebViewer
Aplicação que roda entre páginas da web em uma raspberry pi

## Como usar:
### Em uma nova máquina:
Caso você esteja rodando pela primeira vez, o script funcionará em qualquer máquina que possua Chromium, Unclutter, Xdotool e Xet. 

Se você estiver rodando em um Raspberry Pi (como é esperado) com uma imagem do Raspbian, ou qualquer outra baseada em Debian, você não precisa intalar o Chromium nem o Xset, pois já vem de fábrica. Porém é necessário instalar o Xdotool e o Unclutter.

Basta executar os seguintes comando:
```
sudo apt-get install xdotool, unclutter
```
A partir daqui, você conseguirá executar o script usando o bash.

### Automatizando a aplicação:
O intúito dessa aplicação é que ela fique rodando continuamente em uma máquina durante um período grande de dias. Seria extremamente inconveniente ter que ligar a rasp, ligar a tv e rodar o script, tudo manualmente.

Por isso, foi usado uma série de estratégias para corrigir isso.

#### Para executar o scipt automaticamente ao ligar a rasp:
Abra o terminal e execute o comando:
```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
Aqui você entrará num arquivo que é chamado toda vez que a interface gráfica for inicializada. 

Nele já estão autodefinidos alguns comandos. Coloque em algum lugar no meio (arbitrariamente) o seguinte código:
```
@/bin/bash /home/pi/main.shh
```
Sendo que a primeira parte do comando é a localização do bash, e a segunda parte é a localização para o arquivo 
__main.sh__ (altere se necessário).
#### Ligar e desligar a tv automáticamente:
Foram usados dois artifícios para isso. Para desligar a TV, foi setado o timer dela para desligar todo dia às 10h da noite durante segunda à sexta. Essa configuração depende do modelo da TV, mas é padrão que a maioria delas tenham.

Para ligar a TV, foi necessário usar a Rasp. Simplesmente usamos CronJobs para reiniciar à raspberry, de segunda à sexta, às 7:30 da manhã. Quando a Raspberry reinicia, ela automáticamente ligará a TV (se essa possuir compatbilidade CEC), e como foi configurado antes, o script sempre irá executar ao iniciar a rasp.

A configuração do CronJobs pode ser chamado num terminal com:
```sudo crontab -e```
Se for sua primeira vez usando o comando, ele pedirá pra selecionar qual editor você quer usar, o mais simples é nano, como o próprio terminal sugere.

Isso abrirá um documento com um monte de comentários explicando a sua utilização. No final, adicione isso:
```30 07 * * 1,2,3,4,5 sudo reboot```

Essa estratégia é boa também porque garante que todo dia as páginas tenham uma chance de se atualizar.
