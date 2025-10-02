objects = mainWindow.py expControl.py resControl.py

all: $(objects)
.PHONY: all

$(objects): %.py: ui/%.ui
	pyside6-uic $< -o $@

clean:
	rm -f $(objects)
