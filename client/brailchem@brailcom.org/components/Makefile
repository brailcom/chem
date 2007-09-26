xpidl = /usr/lib/xulrunner/xpidl

all: nsIBrailchem.xpt

%.xpt: %.idl
	$(xpidl) -m typelib -w -v -o nsIBrailchem -I /usr/share/idl/xulrunner -I /usr/lib/xulrunner/idl $<

clean:
	rm -f *.xpt

.PHONY: all clean
