# 8 Puzzle megoldása A* algoritmussal

A program egy adott állapotból eljut a 8 Puzzle kezdeti állapotába:</br>
1 2 3</br>
4 5 6</br>
7 8 0

## Parancssori argumentumok

<b>–input \<FILE\></b>: a kezdeti állapotot tartalmazó állomány neve. Ha a kapcsoló hiányzik, a standard bemenetről
olvassa be a kezdeti állapotot.

<b>–solseq</b>: a standard kimenetre írja a teljes megoldási szekvenciát

<b>–pcost</b>: a standard kimenetre írja a megoldás költségét

<b>–nvisited</b>: a standard kimenetre írja a meglátogatott csomópontok számát

<b>–h \<H\></b>: a heurisztika típusa. Ha H=1, használja a „rossz helyen levő csempék száma” heurisztikát. Ha
Ha H=2, használja a Manhattan heurisztikát.
  
<b>–rand \<N\> \<M\></b> egy véletlenszerű, N méretű állapotot ír ki a standard kimenetre. M a véletlenszerű
tologatások számát jelenti.
  
## Eredmények

2 4 3</br>
1 8 5</br>
7 0 6</br>

pcost: 7</br>
nvisited: 10

2 3 6</br>
7 0 8</br>
4 1 5</br>

pcost: 14</br>
nvisited: 63</br>

0 1 2</br>
5 8 7</br>
3 6 4</br>

pcost: 22 </br>
nvisited: 792 </br>

