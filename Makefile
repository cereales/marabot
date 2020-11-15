EXEC=python3

all: start

start:
	@ $(EXEC) bot.py > log 2>&1 &
	@ echo "Bot running."

install:
	$(EXEC) -m pip install discord
	$(EXEC) -m pip install discord.py
	$(EXEC) -m pip install matplotlib
	apt install python3-numpy

update:
	$(EXEC) -m pip install --upgrade pip
	$(EXEC) -m pip install --upgrade discord
	$(EXEC) -m pip install --upgrade discord.py
	$(EXEC) -m pip install --upgrade matplotlib

