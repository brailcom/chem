domain := brailchem
mo_files := $(shell ls *.po | sed 's/\(.*\)\.\(.*\)\.po/\2\/LC_MESSAGES\/\1.mo/')
src_files := $(shell ls ../src/*.py)

all: $(mo_files)

%/LC_MESSAGES/$(domain).mo: $(domain).%.po
	mkdir -p $*/LC_MESSAGES/
	msgfmt -v $(domain).$*.po -o $@

%.po: brailchem.pot
	msgmerge -q --update $@ $< && touch $@

%.pot:
	xgettext $(src_files) -o $@

clean:
	rm -f *.pot

pot: brailchem.pot