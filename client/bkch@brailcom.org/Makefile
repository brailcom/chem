xpiarchive = ../bkch.xpi

all:
	$(MAKE) -C components
	rm -f $(xpiarchive)
	zip -r $(xpiarchive) *

clean:
	rm -f $(xpiarchive)

.PHONY: all clean
