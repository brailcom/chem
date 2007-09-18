xpidl = /usr/lib/xulrunner/xpidl

all: nsIBkchem.xpt

%.xpt: %.idl
	$(xpidl) -m typelib -w -v -o nsIBkchem -I /usr/share/idl/xulrunner -I /usr/lib/xulrunner/idl $<

clean:
	rm -f *.xpt

.PHONY: all clean
