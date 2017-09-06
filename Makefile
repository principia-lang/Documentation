FILES=$(shell find doc -name '*.md' -type f -print | sort)

.PHONY: all refresh watch

all: build/doc.html

build/doc.md: ${FILES}
	cat $^ > $@

%.html: %.md
	pandoc --from=markdown --to=html5 --standalone --toc --smart --section-divs --css=../2pi.css --mathjax $< -o $@

refresh: all
	xdotool key --window $(shell xdotool search --name "Report" | head -1) F5

watch: refresh
	while : ; do inotifywait -e close_write doc ; make refresh ; done
