xpidl = /usr/lib/xulrunner/xpidl

all: nsIBkchem.xpt

%.xpt: %.idl
	$(xpidl) -m typelib -w -v -o nsIBkchem -I /usr/share/idl/xulrunner $<

clean:
	rm -f *.xpt

.PHONY: all clean
