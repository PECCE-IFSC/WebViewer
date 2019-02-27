# WebViewer
Aplicação que roda entre páginas da web em uma raspberry pi

## Como usar:
### Em uma nova máquina:
Caso você esteja rodando pela primeira vez, o script funcionará em qualquer máquina que possua Python3, PyQt5 e PyQt5.QtWebKit instalados.

Se você estiver rodando em um Raspberry Pi (como é esperado) com uma imagem do Raspbian, ou qualquer outra baseada em Debian, você não precisa intalar o Python, já que este vem de fábrica. Porém, você irá precisar instalar as bibliotecas PyQt5 e PyQt5.QtWebKit.

Basta executar os seguintes comandos no terminal (sempre dando enter entre cada linha):
```
sudo apt-get install python3-pyqt5
sudo apt-get install python3-pyqt5.QtWebKit
```
A partir daqui, você conseguirá executar o script usando o compilador do python.

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
@/usr/bin/python3 /home/pi/Documents/main.py
```
Sendo que a primeira parte do comando é a localização do compilador do Python3, e a segunda parte é a localização para o arquivo 
__main.py__ (altere se necessário).
#### Ligar e desligar a tv automáticamente:
Foram usados dois artifícios para isso. Para desligar a TV, foi setado o timer dela para desligar todo dia às 10h da noite durante segunda à sexta. Essa configuração depende do modelo da TV, mas é padrão que a maioria delas tenham.

Para ligar a TV, foi necessário usar a Rasp. Simplesmente usamos CronJobs para reiniciar à raspberry, de segunda à sexta, às 7:30 da manhã. Quando a Raspberry reinicia, ela automáticamente ligará a TV (se essa possuir compatbilidade CEC), e como foi configurado antes, o script sempre irá executar ao iniciar a rasp.

A configuração do CronJobs pode ser chamado num terminal com:
```sudo crontab -e```
Se for sua primeira vez usando o comando, ele pedirá pra selecionar qual editor você quer usar, o mais simples é nano, como o próprio terminal sugere.

Isso abrirá um documento com um monte de comentários explicando a sua utilização. No final, adicione isso:
```30 07 * * 1,2,3,4,5 sudo reboot```

Essa estratégia é boa também porque garante que todo dia as páginas tenham uma chance de se atualizar.
## Como o script funciona:
O código roda nas bibliotecas do PyQt5, que é uma ferramente extremamente poderosa para criar aplicações GUI em Python. Foram utilizados recursos de forma extremamente simples pois a aplicação é extremamente simples.

Primeiro, deve se saber que a aplicação funciona entre duas linhas:
```python
app = QApplication(sys.argv) #Que inicia o loop principal
...
sys.exit(app.exec_()) #Que encerra o loop quando todas as janelas forem fechadas
```
Depois disso, duas classes são utilizadas, _QtWebKit_ e _QTimer_. A primeira fornece tudo que é necessário para que sejam executadas páginas da web em sua formatação planejada, e a segunda fornece uma interface que executa comandos em determinado período de tempo.

A classe _QtWebKit_ é iniciada dentro de uma array e, em seguida, manualmente é mandado carregar as página que serão representadas pelos indíces da array.
```python
pages = [QWebView(), QWebView()] #Inicia a array
pages[0].load(QUrl("http://sites.florianopolis.ifsc.edu.br/pecce/")) #Adiciona  página do PECCE
pages[1].load(QUrl("http://www.florianopolis.ifsc.edu.br/")) #Adiciona a página do IFSC Florianópolis
pages[2].load(QUrl("url_qualquer_aqui")) #Modelo para adicionar novas páginas
```
Os métodos utilizado da classe _QtWebKit_ são load (já explicado), showFullScreen, hide e reload. Cada um deles são extremamente autoexlicativos.

Depois deve-se conhecer a classe _QTimer_. É usado apenas dois métodos dela:
```python
timer.timeout.connect(task) #A interface irá conectar uma função "task" para ser executada ao fim do timer
timer.start(t) #A interface irá iniciar o timer para um tempo t em milisegundos
```

São utilizadas duas funções conectadas à timers. 
A primeira que é arbitrariamente chamada de task, que possui função de alternar entre as páginas carregas: 
```python
index = 0 #É uma varíavel que conta quantas vez a função foi chamada
def task():
    global index
    index +=1 #Aumenta em 1 o index
    pages[index%len(pages)].showFullScreen() #Aqui é chamado o método showFullScreen da classe QtWebKit na array com index "index%len(pages)", o operador a%b retorna o resto da divisão de a por b, que vai variar sempre entre 0 e b-1, navegando perfeitamente 1 em 1 entre as páginas que devem ser exibidas 
    pages[(index-1)%len(pages)].hide() #Aqui é chamado o método hide para esconder a página que tinha sido mostrada anteriormente, usando a mesma lógica do treixo acima
```
E a segunda que é chamada de updateSite, que atualiza as páginas já carregadas:
```python
def updateSite():
    global pages
    for i in pages: #É rodando um for que navegará na array e então chama o método reload da classe
      i.reload()
```

O sistema, portanto, é consideravelmente automático e, se executado dentro dos parâmetros certos, não há porque não funcionar.
