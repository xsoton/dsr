objects = ui_mainWindow.py ui_expControl.py ui_resControl.py ui_timeControl.py

all: $(objects)
.PHONY: all

$(objects): ui_%.py: ui/%.ui
	pyside6-uic $< -o $@

clean:
	rm -f $(objects)
