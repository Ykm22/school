# install bison in ubuntu

sudo apt install bison

# comenzi de rulat

🟢 easier (in WSL) </br>
`python3 compile_and_run.py fisier3.txt`

bison -d analyzer.y -- saves result into analyzer.tab.c and analyzer.tab.h</br>

flex -o analyzer_lex.c analyzer.l </br>

gcc analyzer.tab.c lex.yy.c </br>

./a.out fisier.txt </br>

# Observations

Symbol tables need to be declared in lex, export the functions to the bison which initialize them, and then in `main()` in bison file call the initialization functions
