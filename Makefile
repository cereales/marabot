EXEC=python

all: start

start:
	@ $(EXEC) bot.py 2&> log &
	@ echo "Bot running."

install:
	$(EXEC) -m pip install discord
	$(EXEC) -m pip install matplotlib
	$(EXEC) -m pip install numpy

