EXEC=python

all: start

start:
	@ $(EXEC) bot.py 2&> log &
	@ echo "Bot running."

install:
	$(EXEC) -m pip install discord
	$(EXEC) -m pip install discord.py
	$(EXEC) -m pip install matplotlib
	$(EXEC) -m pip install numpy

update:
	$(EXEC) -m pip install --upgrade pip
	$(EXEC) -m pip install --upgrade discord
	$(EXEC) -m pip install --upgrade discord.py
	$(EXEC) -m pip install --upgrade matplotlib
	$(EXEC) -m pip install --upgrade numpy

