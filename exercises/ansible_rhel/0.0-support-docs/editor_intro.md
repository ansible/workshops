# Editor Alternatives

If you don’t like **Vim** as an editor feel free to use **Nano** or **Midnight Commander** (**mc**) in the SSH terminal. Here is a quick introduction to both. And no, I’ll refuse to talk about Emacs…​ ;-)

## Midnight Commander (mc)

Mc is more then an editor, it’s a file manager. And it has this nice nineties feel about it…​ anyway we’ll focus on editing files here.

To open **mc** at the commandline prompt type:

    # mc

### Basic Editing

Mc is controlled mainly through the function keys. This can pose all kinds of issues when run in a terminal session, e.g. **F10** is most times caught as a shortcut by the terminal window.

To work around this:

  - Try the combination **ESC** **0** to get **F10**. Don’t hold **ESC**\!

  - Use the mouse, all **mc** keys should be clickable, even if they don’t look it.

To create a new file:

  - Type `touch filename` in the command field to create an empty file

  - Navigate with the **arrow keys** in one of the panes to the new file

  - Hit (or click) **F4** to start editing the file

To save a file:

  - Hit (or click) **F2** and confirm with **Enter**

To exit edit mode with or without saving:

  - Hit **ESC** **0** or click **F10**

  - If you did any changes you will be asked "Save before Close?".

  - Choose one of the options "Yes, No, Cancel" by moving with the **arrow** or **Tab** keys (or click)

Copy text internally:

  - Position the cursor where you want to start to copy

  - Hit (or click) **F3** to start selecting

  - Move the cursor to highlight/select the text you want to copy

  - Hit (or click) **F3** again to stop selecting

Paste text internally:

  - Position the cursor where you want to paste the text

  - Hit (or click) **F5** to paste a copy of the text

  - Hit (or select) **F6** to cut the text and paste it here

Copy text from external source:

  - mark the text with the mouse, e.g. from the lab guide

  - **right-click → Copy**

Paste text from external source:

  - Click **Edit → Paste** in the terminal menu at the top

## Short Intro to the Nano Editor

If you don’t like **Vim** and you feel too young for **Midnight Commander** use **Nano**, a simple to use command line editor.

### Basic Commands

> **Tip**
> 
> **Ctrl-\<n\>** or **Alt-\<n\>** means press and hold the Control or Alt key and then press the character after the dash.

To create a new file or open an existing file:

    # nano playbook.yml

> **Tip**
> 
> When Nano asks for confirmation, it expects a **y** for yes or **n** for no.

To save the current file in Nano:

  - Type **Ctrl-o**

> **Tip**
> 
> Depending if the file was changed or not Nano will ask for confirmation and the file name.

To leave Nano without saving the file (if something went wrong while editing and you just want out without changing anything):

  - Type **Ctrl-x** **n** **Enter**

Copy and paste external text:

  - mark the text with the mouse, e.g. from the lab guide

  - **right-click → Copy**

  - **right-click** into the Nano terminal window, then click **Paste**

----

[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md#section-1---ansible-engine-exercises)
