bdf_to_header.py

Version 0.1

Copyright (c) 2025 Sporos Tech, Peter de Vroomen

This program translates fixed-size font files in the .BDF
format (Bitmap Distribution Format) to a C/C++ header file
in either a basic structured format or a format that is
directly usable by the FabGL library.


Important note on the supported format:

The parser is relatively sophisticated, but the .BDF format
is quite versatile and the parser can only handle certain
formats.

Specifically, it cannot handle .BDF font files with sparse
character information (e.g. files where the pixels of the
characters are given as a sub-rectangle inside the larger
rectangle). I have only ever found one .BDF file that was
like that, and I wasn't interested in it, so I didn't spend
the effort to add support for such files.

In case this script cannot handle a certain .BDF format,
maybe you could try loading it in e.g. FontForge and re-
saving it. I never tried, so this is just a suggestion.

If that doesn't work, and you really, really want to have
the font and am prepared to spend some time for it, you
can manually edit the file. It is not complex or hard, but
just takes a lot of time, and a calculator that can convert
hex to bin and vice versa.


About the Adobe Glyph List for ISO Latin 1 character set,
which is used in the BDF format:

https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format

The position of the items in the list correspond to the
extended ISO Lating 1 ascii character set.
Apart from the first 32 characters. These names are not
in the Adobe Glyph List, but are the names as given for
ascii control characters.
Most character sets do not have printable characters for
these control characters, but we can show their hexadecimal
value in the font. Character marked with a * are characters
whose glyph name is not named in the Adobe Glyph List.
Characteres marked with a # are not in the old Adobe Glyph List,
but are in the newer version of the Adobe Glyph List.
A value of "unused" means that there is no glyph defined
for that character.

Source:

  https:#github.com/adobe-type-tools/agl-specification

  Adobe Glyph List:
    https:#github.com/adobe-type-tools/agl-aglfn/blob/master/glyphlist.txt
  Adobe Glyph List for New Fonts:
    https://github.com/adobe-type-tools/agl-aglfn/blob/master/aglfn.txt

About the NNNNN.charset files:

This is a file that contains 256 lines with Adobe glyph
description names for every character in the character set
(this script assumes 256 characters in a character set).

Each line starts with a - and ends with a -. In between those,
the line lists the Adobe glyph description names, separated
with a -.

You would expect there to be only one name per character, but
I have found empirically that sometimes there are long and
short names for a character, for instance 'nbspace' and
'nobreakspace', or 'dc1' and 'devicecontrolone'.

In other cases, I have found that some characters do not exist
in a .BDF file, but the file does contain an alternative with
a different name.

There is also the special name 'unused', which means to use
the replacement character for the specific character in the
character set. Basically any glyph description name that is
not found in the .BDF file will be replaced with the
replacement character, specifying 'unused' is just for
readability purposes.

The replacement character is the glyph description name
'uniFFFD' by default, but can be changed to any other glyph
description name. Some .BDF files don't specify the 'uniFFFD'
character, in which case the script will just use an empty
bitmap (a space, basically).

The lines in the .charset file are parsed from left to right,
so if a .BDF file contains both glyphs, the first is taken.

For example:

  -A-                     The uppercase letter A
  -a-                     The lowercase letter a
  -question-              A question mark
  -ccedilla-              The lowercase ç
  -Ccedilla-              The uppercase Ç
  -germandbls-ssharp-     The ß, which in some .BDF files is
                          named 'germandbls and others 'ssharp'
  -Adieresis-Adiaeresis-  The Ä, which in some .BDF files is
                          spelled as 'Adieresis' and others as
                          'Adiaeresis'.
  -bullet-apl_jot-        The ·, which is normally given as
                          'bullet', but is missing in some fonts.
                          A good alternative is the 'apl_jot'
                          glyph.

The file 'cp-1252.charset' defines the glyphs such that the output
file will contain the Windows Code Page 1252 character set, which is
close to the ISO-8859-1 character set.

The file 'cp-437.charset' defines the original ms-dos character set
with the well-known line drawing graphics.

It's easy to create another file to create other code page character
sets. As long as you know the names of the Adobe glyph description
names.

For reference, here is the content of the 'cp-1252.charset' file. If
the 'cp-1252.charset' file was not distributed together with this
script, you can recreate it using this list. Just copy all, then paste
it in a text file named 'cp-1252.charset'.

-null-char0-
-soh-startofheader-
-stx-startoftext-
-etx-endoftext-
-eot-endoftransmission-
-enq-enquiry-
-ack-acknowledge-
-bel-bell-
-bs-backspace-
-tab-horizontaltab-
-lf-linefeed-
-vt-verticaltab-
-ff-formfeed-
-cr-carriagereturn-
-shiftout-downshift-
-shiftin-upshift-
-dle-datalinkescape-
-dc1-devicecontrolone-
-dc2-devicecontroltwo-
-dc3-devicecontrolthree-
-dc4-devicecontrolfour-
-nak-negativeacknowledge-
-syn-synchronousidle-
-eob-endoftransmissionblock-
-can-cancel-
-eom-endofmedium-
-sub-substitute-
-esc-escape-
-fs-fileseparator-
-gs-groupseparator-
-rs-recordseparator-
-us-unitseparator-
-space-
-exclam-
-quotedbl-
-numbersign-
-dollar-
-percent-
-ampersand-
-quotesingle-apostrophe-
-parenleft-
-parenright-
-asterisk-
-plus-
-comma-
-hyphen-minus-
-period-
-slash-
-0-zero-
-1-one-
-2-two-
-3-three-
-4-four-
-5-five-
-6-six-
-7-seven-
-8-eight-
-9-nine-
-colon-
-semicolon-
-less-
-equal-
-greater-
-question-
-at-
-A-
-B-
-C-
-D-
-E-
-F-
-G-
-H-
-I-
-J-
-K-
-L-
-M-
-N-
-O-
-P-
-Q-
-R-
-S-
-T-
-U-
-V-
-W-
-X-
-Y-
-Z-
-bracketleft-
-backslash-
-bracketright-
-asciicircum-
-underscore-
-grave-
-a-
-b-
-c-
-d-
-e-
-f-
-g-
-h-
-i-
-j-
-k-
-l-
-m-
-n-
-o-
-p-
-q-
-r-
-s-
-t-
-u-
-v-
-w-
-x-
-y-
-z-
-braceleft-
-bar-
-braceright-
-asciitilde-
-del-delete-
-Euro-
-unused-
-quotesinglbase-
-florin-
-quotedblbase-
-ellipsis-
-dagger-
-daggerdbl-
-circumflex-
-perthousand-
-Scaron-
-guilsinglleft-
-OE-
-unused-
-Zcaron-
-unused-
-unused-
-quoteleft-
-quoteright-
-quotedblleft-
-quotedblright-
-bullet-apl_jot-
-endash-
-emdash-apl_midhbar-
-tilde-
-trademark-
-scaron-
-guilsinglright-
-oe-
-unused-
-zcaron-
-Ydieresis-Ydiaeresis-
-nbspace-nobreakspace-
-invertedexclam-exclamdown-
-cent-
-sterling-
-currency-
-yen-
-brokenbar-
-section-
-dieresis-diaeresis-
-copyright-
-ordfeminine-feminine-
-guillemotleft-
-logicalnot-notsign-
-softhyphen-SHY-
-registered-
-macron-
-degree-
-plusminus-
-twosuperior-
-threesuperior-
-acute-
-mu-
-paragraph-
-periodcentered-
-cedilla-
-onesuperior-
-ordmasculine-masculine-
-guillemotright-
-onequarter-
-onehalf-
-threequarters-
-questiondown-
-Agrave-
-Aacute-
-Acircumflex-
-Atilde-
-Adieresis-Adiaeresis-
-Aring-
-AE-
-Ccedilla-
-Egrave-
-Eacute-
-Ecircumflex-
-Edieresis-Ediaeresis-
-Igrave-
-Iacute-
-Icircumflex-
-Idieresis-Idiaeresis-
-Eth-ETH-
-Ntilde-
-Ograve-
-Oacute-
-Ocircumflex-
-Otilde-
-Odieresis-Odiaeresis-
-multiply-multiplication-
-Oslash-Ooblique-
-Ugrave-
-Uacute-
-Ucircumflex-
-Udieresis-Udiaeresis-
-Yacute-
-Thorn-THORN-
-germandbls-ssharp-
-agrave-
-aacute-
-acircumflex-
-atilde-
-adieresis-adiaeresis-
-aring-
-ae-
-ccedilla-
-egrave-
-eacute-
-ecircumflex-
-edieresis-ediaeresis-
-igrave-
-iacute-
-icircumflex-
-idieresis-idiaeresis-
-eth-
-ntilde-
-ograve-
-oacute-
-ocircumflex-
-otilde-
-odieresis-odiaeresis-
-divide-division-
-oslash-
-ugrave-
-uacute-
-ucircumflex-
-udieresis-udiaeresis-
-yacute-
-thorn-
-ydieresis-ydiaeresis-

