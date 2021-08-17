########################################################
# Makefile for ansible/workshops
#
# useful targets
#   make show-translated-folder -- show list of exercises with localization enabled
#   make generate-po ------------- generate language specific po file
#   make needs-translation ------- generate list of file with untranslated or fuzzy string for a specific language
#   make apply-translation ------- Take PO file as entry and generate a localized README.<locale>.md file
#   make clean-translation ------- Removes the locales/ folder in each exercise folder
#
########################################################

BASE_PATH ?= '.'
TRANSLATED_FOLDERS := $(shell find $(BASE_PATH) -name 'po4a.cfg' -exec dirname {} \;)
EXISTING_PO_FILES := $(shell find $(BASE_PATH) -name '*.po')

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
needs-translation:
	for file in $(EXISTING_PO_FILES); do \
		python pooneliner.py $$file ; \
	done

.SILENT:
apply-translation:
	for translated_folder in $(TRANSLATED_FOLDERS); do \
		pushd 2>&1>/dev/null $$translated_folder && \
		po4a po4a.cfg --no-update 2>&1>/dev/null && \
		popd 2>&1>/dev/null ; \
	done

.SILENT:
clean-translation:
	for translated_folder in $(TRANSLATED_FOLDERS); do \
		pushd 2>&1>/dev/null $$translated_folder && \
		rm -rf locales && \
		popd 2>&1>/dev/null ; \
	done
