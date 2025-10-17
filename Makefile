objects = ui_DSRControl.py ui_K6482Control.py ui_MainWindow.py ui_RespControl.py ui_TimeControl.py

all: $(objects)
.PHONY: all

$(objects): ui_%.py: ui/%.ui
	pyside6-uic $< -o $@

clean:
	rm -f $(objects)
