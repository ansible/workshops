TRANSLATED_FOLDERS := $(shell find . -name 'po4a.cfg' -exec dirname {} \;)
EXISTING_PO_FILES := $(shell find . -name '*.po')

show-translated-folders:
	@echo $(TRANSLATED_FOLDERS)

.SILENT:
generate-po:
	for translated_folder in $(TRANSLATED_FOLDERS); do \
		pushd 2>&1>/dev/null $$translated_folder && \
		po4a po4a.cfg --no-translations 2>&1>/dev/null && \
		popd 2>&1>/dev/null ; \
	done

.SILENT:
list-po-needs-translation:
	for file in $(EXISTING_PO_FILES); do \
		python pooneliner.py $$file ; \
	done

.SILENT:
translation:
	for translated_folder in $(TRANSLATED_FOLDERS); do \
		pushd 2>&1>/dev/null $$translated_folder && \
		po4a po4a.cfg --no-update 2>&1>/dev/null && \
		popd 2>&1>/dev/null ; \
	done

.SILENT:
translation-clean:
	for translated_folder in $(TRANSLATED_FOLDERS); do \
		pushd 2>&1>/dev/null $$translated_folder && \
		rm -rf locales && \
		popd 2>&1>/dev/null ; \
	done

