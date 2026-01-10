#!/usr/bin/env python

# bdf_to_header.py
#
# Version 0.1
#
# Copyright (c) 2025 Sporos Tech, Peter de Vroomen
#
# This program translates fixed-size font files in the .BDF
# format (Bitmap Distribution Format) to a C/C++ header file
# in either a basic structured format or a format that is
# directly usable by the FabGL library.
#
#
# Important note on the supported format:
#
# The parser is relatively sophisticated, but the .BDF format
# is quite versatile and the parser can only handle certain
# formats.
#
# Specifically, it cannot handle .BDF font files with sparse
# character information (e.g. files where the pixels of the
# characters are given as a sub-rectangle inside the larger
# rectangle). I have only ever found one .BDF file that was
# like that, and I wasn't interested in it, so I didn't spend
# the effort to add support for such files.
#
# In case this script cannot handle a certain .BDF format,
# maybe you could try loading it in e.g. FontForge and re-
# saving it. I never tried, so this is just a suggestion.
#
# If that doesn't work, and you really, really want to have
# the font and am prepared to spend some time for it, you
# can manually edit the file. It is not complex or hard, but
# just takes a lot of time, and a calculator that can convert
# hex to bin and vice versa.
#
#
# About the Adobe Glyph List for ISO Latin 1 character set,
# which is used in the BDF format:
#
# https://en.wikipedia.org/wiki/Glyph_Bitmap_Distribution_Format
#
# The position of the items in the list correspond to the
# extended ISO Lating 1 ascii character set.
# Apart from the first 32 characters. These names are not
# in the Adobe Glyph List, but are the names as given for
# ascii control characters.
# Most character sets do not have printable characters for
# these control characters, but we can show their hexadecimal
# value in the font. Character marked with a * are characters
# whose glyph name is not named in the Adobe Glyph List.
# Characteres marked with a # are not in the old Adobe Glyph List,
# but are in the newer version of the Adobe Glyph List.
# A value of "unused" means that there is no glyph defined
# for that character.
#
# Source:
#
#   https:#github.com/adobe-type-tools/agl-specification
#
#   Adobe Glyph List:
#     https:#github.com/adobe-type-tools/agl-aglfn/blob/master/glyphlist.txt
#   Adobe Glyph List for New Fonts:
#     https://github.com/adobe-type-tools/agl-aglfn/blob/master/aglfn.txt
#
# About the NNNNN.charset files:
#
# This is a file that contains 256 lines with Adobe glyph
# description names for every character in the character set
# (this script assumes 256 characters in a character set).
#
# Each line starts with a - and ends with a -. In between those,
# the line lists the Adobe glyph description names, separated
# with a -.
#
# You would expect there to be only one name per character, but
# I have found empirically that sometimes there are long and
# short names for a character, for instance 'nbspace' and
# 'nobreakspace', or 'dc1' and 'devicecontrolone'.
#
# In other cases, I have found that some characters do not exist
# in a .BDF file, but the file does contain an alternative with
# a different name.
#
# There is also the special name 'unused', which means to use
# the replacement character for the specific character in the
# character set. Basically any glyph description name that is
# not found in the .BDF file will be replaced with the
# replacement character, specifying 'unused' is just for
# readability purposes.
#
# The replacement character is the glyph description name
# 'uniFFFD' by default, but can be changed to any other glyph
# description name. Some .BDF files don't specify the 'uniFFFD'
# character, in which case the script will just use an empty
# bitmap (a space, basically).
#
# The lines in the .charset file are parsed from left to right,
# so if a .BDF file contains both glyphs, the first is taken.
#
# For example:
#
#   -A-                     The uppercase letter A
#   -a-                     The lowercase letter a
#   -question-              A question mark
#   -ccedilla-              The lowercase ç
#   -Ccedilla-              The uppercase Ç
#   -germandbls-ssharp-     The ß, which in some .BDF files is
#                           named 'germandbls and others 'ssharp'
#   -Adieresis-Adiaeresis-  The Ä, which in some .BDF files is
#                           spelled as 'Adieresis' and others as
#                           'Adiaeresis'.
#   -bullet-apl_jot-        The ·, which is normally given as
#                           'bullet', but is missing in some fonts.
#                           A good alternative is the 'apl_jot'
#                           glyph.
#
# The file 'cp-1252.charset' defines the glyphs such that the output
# file will contain the Windows Code Page 1252 character set, which is
# close to the ISO-8859-1 character set.
#
# The file 'cp-437.charset' defines the original ms-dos character set
# with the well-known line drawing graphics.
#
# It's easy to create another file to create other code page character
# sets. As long as you know the names of the Adobe glyph description
# names.
#
# For reference, here is the content of the 'cp-1252.charset' file. If
# the 'cp-1252.charset' file was not distributed together with this
# script, you can recreate it using this list. Just copy all, then paste
# it in a text file named 'cp-1252.charset', and be sure to remove the
# leading '#' and space from each line.
#
# -null-char0-
# -soh-startofheader-
# -stx-startoftext-
# -etx-endoftext-
# -eot-endoftransmission-
# -enq-enquiry-
# -ack-acknowledge-
# -bel-bell-
# -bs-backspace-
# -tab-horizontaltab-
# -lf-linefeed-
# -vt-verticaltab-
# -ff-formfeed-
# -cr-carriagereturn-
# -shiftout-downshift-
# -shiftin-upshift-
# -dle-datalinkescape-
# -dc1-devicecontrolone-
# -dc2-devicecontroltwo-
# -dc3-devicecontrolthree-
# -dc4-devicecontrolfour-
# -nak-negativeacknowledge-
# -syn-synchronousidle-
# -eob-endoftransmissionblock-
# -can-cancel-
# -eom-endofmedium-
# -sub-substitute-
# -esc-escape-
# -fs-fileseparator-
# -gs-groupseparator-
# -rs-recordseparator-
# -us-unitseparator-
# -space-
# -exclam-
# -quotedbl-
# -numbersign-
# -dollar-
# -percent-
# -ampersand-
# -quotesingle-apostrophe-
# -parenleft-
# -parenright-
# -asterisk-
# -plus-
# -comma-
# -hyphen-minus-
# -period-
# -slash-
# -0-zero-
# -1-one-
# -2-two-
# -3-three-
# -4-four-
# -5-five-
# -6-six-
# -7-seven-
# -8-eight-
# -9-nine-
# -colon-
# -semicolon-
# -less-
# -equal-
# -greater-
# -question-
# -at-
# -A-
# -B-
# -C-
# -D-
# -E-
# -F-
# -G-
# -H-
# -I-
# -J-
# -K-
# -L-
# -M-
# -N-
# -O-
# -P-
# -Q-
# -R-
# -S-
# -T-
# -U-
# -V-
# -W-
# -X-
# -Y-
# -Z-
# -bracketleft-
# -backslash-
# -bracketright-
# -asciicircum-
# -underscore-
# -grave-
# -a-
# -b-
# -c-
# -d-
# -e-
# -f-
# -g-
# -h-
# -i-
# -j-
# -k-
# -l-
# -m-
# -n-
# -o-
# -p-
# -q-
# -r-
# -s-
# -t-
# -u-
# -v-
# -w-
# -x-
# -y-
# -z-
# -braceleft-
# -bar-
# -braceright-
# -asciitilde-
# -del-delete-
# -Euro-
# -unused-
# -quotesinglbase-
# -florin-
# -quotedblbase-
# -ellipsis-
# -dagger-
# -daggerdbl-
# -circumflex-
# -perthousand-
# -Scaron-
# -guilsinglleft-
# -OE-
# -unused-
# -Zcaron-
# -unused-
# -unused-
# -quoteleft-
# -quoteright-
# -quotedblleft-
# -quotedblright-
# -bullet-apl_jot-
# -endash-
# -emdash-apl_midhbar-
# -tilde-
# -trademark-
# -scaron-
# -guilsinglright-
# -oe-
# -unused-
# -zcaron-
# -Ydieresis-Ydiaeresis-
# -nbspace-nobreakspace-
# -invertedexclam-exclamdown-
# -cent-
# -sterling-
# -currency-
# -yen-
# -brokenbar-
# -section-
# -dieresis-diaeresis-
# -copyright-
# -ordfeminine-feminine-
# -guillemotleft-
# -logicalnot-notsign-
# -softhyphen-SHY-
# -registered-
# -macron-
# -degree-
# -plusminus-
# -twosuperior-
# -threesuperior-
# -acute-
# -mu-
# -paragraph-
# -periodcentered-
# -cedilla-
# -onesuperior-
# -ordmasculine-masculine-
# -guillemotright-
# -onequarter-
# -onehalf-
# -threequarters-
# -questiondown-
# -Agrave-
# -Aacute-
# -Acircumflex-
# -Atilde-
# -Adieresis-Adiaeresis-
# -Aring-
# -AE-
# -Ccedilla-
# -Egrave-
# -Eacute-
# -Ecircumflex-
# -Edieresis-Ediaeresis-
# -Igrave-
# -Iacute-
# -Icircumflex-
# -Idieresis-Idiaeresis-
# -Eth-ETH-
# -Ntilde-
# -Ograve-
# -Oacute-
# -Ocircumflex-
# -Otilde-
# -Odieresis-Odiaeresis-
# -multiply-multiplication-
# -Oslash-Ooblique-
# -Ugrave-
# -Uacute-
# -Ucircumflex-
# -Udieresis-Udiaeresis-
# -Yacute-
# -Thorn-THORN-
# -germandbls-ssharp-
# -agrave-
# -aacute-
# -acircumflex-
# -atilde-
# -adieresis-adiaeresis-
# -aring-
# -ae-
# -ccedilla-
# -egrave-
# -eacute-
# -ecircumflex-
# -edieresis-ediaeresis-
# -igrave-
# -iacute-
# -icircumflex-
# -idieresis-idiaeresis-
# -eth-
# -ntilde-
# -ograve-
# -oacute-
# -ocircumflex-
# -otilde-
# -odieresis-odiaeresis-
# -divide-division-
# -oslash-
# -ugrave-
# -uacute-
# -ucircumflex-
# -udieresis-udiaeresis-
# -yacute-
# -thorn-
# -ydieresis-ydiaeresis-

import code
import codecs
import os
import pprint
import sys
import getopt

inputfile = ''
outputfile = ''
replacement_char = "uniFFFD"
glyph_description_filename = "cp-1252.charset"

header_file_format = "structured"

adobe_glyph_descriptions = []

width_in_pixels = 0
height_in_pixels = 0
left_offset = 0
bottom_offset = 0
width_in_bytes = 0
height_in_lines = 0
font_descent = 0
font_ascent = 0

bitmap_bytes = []
aggregated_bitmap_bytes = [[] for _ in range(256)]

replacement_char_bytes = []

parsed_codes = []
skipped_codes = []
replacement_char_codes = []


class ParseError(Exception):
    reason: str

def read_charset(filename):
    charset = []
    try:
      with open(filename, 'r') as f:
          for line in f:
              line = line.strip()
              if line and not line.startswith('#'):
                  charset.append(line)
    except Exception as e:
      print("Error opening or reading charset file '", filename, "': ", e)
      exit(1)
    return charset

def parse_bounding_box(line):
  items = line.split(" ")
  if items[0] != "FONTBOUNDINGBOX":
    raise ParseError("expected FONTBOUNDINGBOX")
  return (int(items[1]),int(items[2]),int(items[3]), int(items[4]))

def parse_start_char(line):
  items = line.split(" ")
  if items[0] != "STARTCHAR":
    raise ParseError("expected STARTCHAR")
  return items[1]

def parse_encoding(line):
  items = line.split(" ")
  if items[0] != "ENCODING":
    raise ParseError("expected ENCODING")
  return items[1]

def parse_bbx(line):
  items = line.split(" ")
  if items[0] != "BBX":
    raise ParseError("expected BBX")
  return (int(items[1]),int(items[2]),int(items[3]), int(items[4]))

def parse_bitmap(line):
  items = line.split(" ")
  if items[0] != "BITMAP":
    raise ParseError("expected BITMAP")

def parse_bitmap_line(line):
  return bytes.fromhex(line)

def find_ascii_code_by_name(name):

#  try:
#    maybe_bytes = bytes.fromhex(name)
#    if len(maybe_bytes) == 1:
#      ascii_code = maybe_bytes[0]
#      if ascii_code < 256:
#        return ascii_code
#  except:
  for ascii_code in range(0,256):
    if adobe_glyph_descriptions[ascii_code].__contains__("-"+name+"-"):
      return ascii_code

  return -1

def parse_property_line(line):

  global width_in_pixels
  global height_in_pixels
  global left_offset
  global bottom_offset
  global width_in_bytes
  global height_in_lines
  global font_descent
  global font_ascent

  items = line.split(" ")

  if items[0] == "ENDPROPERTIES":
    return "ENDPROPERTIES"

  if items[0] == "FONT_ASCENT":
    font_ascent = int(items[1])
    return "FONT_ASCENT"

  if items[0] == "FONT_DESCENT":
    font_descent = int(items[1])
    return "FONT_DESCENT"

  return items[0]


def parse_file(inputfile, outputfile):

  global width_in_pixels
  global height_in_pixels
  global left_offset
  global bottom_offset
  global width_in_bytes
  global height_in_lines

  global current_bitmap_line

  global bitmap_bytes
  global aggregated_bitmap_bytes

  global replacement_char_bytes

  global parsed_codes
  global skipped_codes
  global replacement_char_codes

  ascii_code = 0
  current_bitmap_line = 0

  with open(inputfile) as f:
    lines = f.readlines() # list containing lines of file

    nextExpectation = "FONTBOUNDINGBOX"

    for line in lines:
        line = line.strip() # remove leading/trailing white spaces
        if line:
          if line.startswith(nextExpectation) or nextExpectation == "BITMAPLINE" or nextExpectation == "BITMAPLINESFINISHED" or nextExpectation == "SKIPCHAR" or nextExpectation == "PROPERTIESLINE":
            match nextExpectation:
              case "FONTBOUNDINGBOX":
                try:
                  items = parse_bounding_box(line)
                  nextExpectation = "STARTPROPERTIES"
                except ParseError as e:
                  print("PARSE ERROR:", e.reason)
                  exit(1)
              case "STARTPROPERTIES":
                try:
                  nextExpectation = "PROPERTIESLINE"
                except ParseError as e:
                  print("PARSE ERROR:", e.reason)
                  exit(1)
              case "PROPERTIESLINE":
                try:
                  propertyName = parse_property_line(line)

                  if propertyName == "ENDPROPERTIES":
                    nextExpectation = "STARTCHAR"
                  else:
                    nextExpectation = "PROPERTIESLINE"
                except ParseError as e:
                  print("PARSE ERROR:", e.reason)
                  exit(1)

              case "STARTCHAR":
                try:
                  name = parse_start_char(line)

                  print("\n> glyph: '" + name + "'")

                  if name == replacement_char:
                    print("  > Found replacement character '"+replacement_char+", storing for later.")
                    nextExpectation = "ENCODING"
                    continue

                  ascii_code = find_ascii_code_by_name(name)
                  if ascii_code == -1:
                    print("  > not required -> skip")
                    skipped_codes.append(name)
                    nextExpectation = "SKIPCHAR"
                    continue

                  print("    Assign to ASCII code: " + str(ascii_code))
                  parsed_codes.append(name + " (" + str(ascii_code) + ")")

                  if len(aggregated_bitmap_bytes[ascii_code]) != 0:
                    print("WARNING: ASCII code ", ascii_code, " already has a glyph assigned - skipping")
                    nextExpectation = "SKIPCHAR"
                  else:
                    nextExpectation = "ENCODING"
                except ParseError as e:
                  print("PARSE ERROR:", e.reason)
                  exit(1)
              case "ENCODING":
                try:
                  encoding = parse_encoding(line)
                  nextExpectation = "BBX"
                except ParseError as e:
                  print("PARSE ERROR:", e.reason)
                  exit(1)
              case "BBX":
                try:
                  items = parse_bbx(line)

                  print("    bounding box (w,h,x,y): (" + str(items[0]) + "," + str(items[1]) + "," + str(items[2]) + "," + str(items[3]) + ")")

                  width_in_pixels = items[0]
                  height_in_pixels = items[1]
                  left_offset = items[2]
                  bottom_offset = items[3]

                  width_in_bytes = (width_in_pixels + 7) // 8
                  height_in_lines = height_in_pixels

                  nextExpectation = "BITMAP"
                except ParseError as e:
                  print("PARSE ERROR:", e.reason)
                  exit(1)
              case "BITMAP":
                try:
                  parse_bitmap(line)

                  current_bitmap_line = 0
                  bitmap_bytes = [[0] * width_in_bytes for _ in range(height_in_lines)]

                  nextExpectation = "BITMAPLINE"
                except ParseError as e:
                  print("PARSE ERROR:", e.reason)
                  exit(1)
              case "BITMAPLINE":
                try:
                  bytes = parse_bitmap_line(line)
                  for byte_index in range(len(bytes)):
                    bitmap_bytes[current_bitmap_line][byte_index] = bytes[byte_index]

                  current_bitmap_line += 1

                  if current_bitmap_line >= height_in_lines:
                    print("    bytes: ", bitmap_bytes)

                    if name == replacement_char:
                      replacement_char_bytes = bitmap_bytes
                    else:
                      aggregated_bitmap_bytes[ascii_code] = bitmap_bytes

                    nextExpectation = "ENDCHAR"
                  else:
                    nextExpectation = "BITMAPLINE"
                except ParseError as e:
                  print("PARSE ERROR:", e.reason)
                  exit(1)
              case "ENDCHAR":
                if line != "ENDCHAR":
                  print("PARSE ERROR: expected ENDCHAR")
                  exit(1)
                nextExpectation = "STARTCHAR"
              case "SKIPCHAR":
                nextExpectation = "STARTCHAR"
              case _:
                print("Unknown expectation state: ", nextExpectation)
                exit(1)

  print("\nFinished parsing file.");

def write_output_file_structured():

  global inputfile
  global outputfile
  global glyph_description_filename
  global adobe_glyph_descriptions
  global replacement_char

  global width_in_pixels
  global height_in_pixels
  global left_offset
  global bottom_offset
  global width_in_bytes
  global height_in_lines

  global current_bitmap_line

  global bitmap_bytes
  global aggregated_bitmap_bytes

  global replacement_char_bytes

  global parsed_codes
  global skipped_codes
  global replacement_char_codes

  print("\nWriting output file: ", outputfile)

  with open(outputfile, "w") as f:
    f.write("#pragma once\n\n")

    f.write("// Generated by bdf_to_header.py from '"+str(inputfile)+"'\n")
    f.write("//\n")
    f.write("// Font info:\n")
    f.write("//\n")
    f.write("//   width in pixels         = "+str(width_in_pixels)+"\n")
    f.write("//   height in pixels        = "+str(height_in_pixels)+"\n")
    f.write("//   left offset in pixels   = "+str(left_offset)+"\n")
    f.write("//   bottom offset in pixels = "+str(bottom_offset)+"\n")
    f.write("//   ascent                  = "+str(font_ascent)+"\n")
    f.write("//   descent                 = "+str(font_descent)+"\n")
    f.write("//\n")
    f.write("//   width in bytes          = "+str(width_in_bytes)+"\n")
    f.write("//   height in lines         = "+str(height_in_lines)+"\n")
    f.write("//\n")
    f.write("//   replacement char        = "+replacement_char+"\n")
    f.write("//\n")
    f.write("// Bitmap data for ASCII characters 0-255:\n")
    f.write("\n")

    fontStructName = "FONT_" + mangle_filename(os.path.splitext(os.path.basename(outputfile))[0])

    f.write("static const uint8_t " + fontStructName + "_DATA[256][")
    f.write(str(height_in_lines))
    f.write("][")
    f.write(str(width_in_bytes))
    f.write("] = {\n\n")

    for ascii_code in range(0,256):

      bitmap_bytes = aggregated_bitmap_bytes[ascii_code]

      f.write("  // ASCII code ")
      f.write(str(ascii_code)+" (0x"+ascii_code.to_bytes(1, byteorder='big').hex()+") ("+adobe_glyph_descriptions[ascii_code]+")")

      if len(bitmap_bytes) == 0:
        f.write(" - no bitmap defined - using 'replacement char'")
        if len(replacement_char_bytes) > 0:
          replacement_char_codes.append(ascii_code)
          bitmap_bytes = replacement_char_bytes
        else:
          f.write(" - no 'replacement_char' bitmap defined - use empty bitmap")
          bitmap_bytes = [[0] * width_in_bytes for _ in range(height_in_lines)]

      f.write("\n")
      f.write("  {\n")

      for bytes in bitmap_bytes:
        f.write("    { ")

        for byte in bytes:
          f.write("0x")
          f.write(f"{byte:02X}")
          if len(bytes) > 1:
            f.write(",")
          f.write(" ")
        f.write("},")

        f.write("      // |")
        bit_count = 0
        for byte in bytes:
          for bit in range(8):
            if byte & (1 << (7 - bit)):
              f.write("#")
            else:
              f.write(" ")
            bit_count += 1
            if bit_count >= width_in_pixels:
              break
        f.write("|\n")

      f.write("  },\n")
    f.write("};\n")

    f.close()

def mangle_filename(name: str) -> str:
    return (name.upper()
            .replace("-", "_")
            .replace(".", "_")
            .replace(" ", "_")
            .replace("@", "_AT_")
            .replace("+", "_PLUS_")
            .replace("#", "_HASH_")
            .replace("$", "_DOLLAR_")
            .replace("%", "_PERCENT_")
            .replace("^", "_CARET_")
            .replace("&", "_AND_")
            .replace("*", "_STAR_")
            .replace("(", "_LPAREN_")
            .replace(")", "_RPAREN_")
            .replace("[", "_LBRACKET_")
            .replace("]", "_RBRACKET_")
            .replace("{", "_LBRACE_")
            .replace("}", "_RBRACE_")
            .replace(";", "_SEMICOLON_")
            .replace(":", "_COLON_")
            .replace("'", "_APOSTROPHE_")
            .replace("\"", "_QUOTE_")
            .replace("<", "_LT_")
            .replace(">", "_GT_")
            .replace(",", "_COMMA_")
            .replace(".", "_DOT_")
            .replace("?", "_QUESTION_")
            .replace("/", "_SLASH_")
            .replace("\\", "_BACKSLASH_")
            .replace("|", "_PIPE_")
            .replace("~", "_TILDE_")
            .replace("`", "_BACKTICK_"))

def write_output_file_fabgl():

  global inputfile
  global outputfile
  global glyph_description_filename
  global adobe_glyph_descriptions
  global replacement_char

  global width_in_pixels
  global height_in_pixels
  global left_offset
  global bottom_offset
  global width_in_bytes
  global height_in_lines
  global font_descent
  global font_ascent

  global current_bitmap_line

  global bitmap_bytes
  global aggregated_bitmap_bytes

  global replacement_char_bytes

  global parsed_codes
  global skipped_codes
  global replacement_char_codes

  print("\nWriting output file: ", outputfile)

  with open(outputfile, "w") as f:
    f.write("#pragma once\n\n")

    f.write("// Generated by bdf_to_header.py from '"+str(inputfile)+"'\n")
    f.write("//\n")
    f.write("// Font info:\n")
    f.write("//\n")
    f.write("//   width in pixels         = "+str(width_in_pixels)+"\n")
    f.write("//   height in pixels        = "+str(height_in_pixels)+"\n")
    f.write("//   left offset in pixels   = "+str(left_offset)+"\n")
    f.write("//   bottom offset in pixels = "+str(bottom_offset)+"\n")
    f.write("//   ascent                  = "+str(font_ascent)+"\n")
    f.write("//   descent                 = "+str(font_descent)+"\n")
    f.write("//\n")
    f.write("//   width in bytes          = "+str(width_in_bytes)+"\n")
    f.write("//   height in lines         = "+str(height_in_lines)+"\n")
    f.write("//\n")
    f.write("//   replacement char        = "+replacement_char+"\n")
    f.write("//\n")
    f.write("// Bitmap data for ASCII characters 0-255\n")
    f.write("\n")

    f.write("namespace fabgl {\n\n")

    f.write("#ifdef FABGL_FONT_INCLUDE_DEFINITION\n\n")

    fontStructName = "FONT_" + mangle_filename(os.path.splitext(os.path.basename(outputfile))[0])

    f.write("static const uint8_t " + fontStructName + "_DATA[] = {\n\n")

    for ascii_code in range(0,256):

      bitmap_bytes = aggregated_bitmap_bytes[ascii_code]

      f.write("  // ASCII code ")
      f.write(str(ascii_code)+" (0x"+ascii_code.to_bytes(1, byteorder='big').hex()+") ("+adobe_glyph_descriptions[ascii_code]+")\n")

      if len(bitmap_bytes) == 0:
        # Use replacement char
        if len(replacement_char_bytes) > 0:
          # Use the stored replacement char
          replacement_char_codes.append(ascii_code)
          bitmap_bytes = replacement_char_bytes
        else:
          # Use empty bitmap if there is no replacement_char
          bitmap_bytes = [[0] * width_in_bytes for _ in range(height_in_lines)]

      for bytes in bitmap_bytes:

        f.write("  ");
        for byte in bytes:
          f.write("0x")
          f.write(f"{byte:02X}")
          if len(bytes) > 0:
            f.write(",")

        f.write("      // |")
        bit_count = 0
        for byte in bytes:
          for bit in range(8):
            if byte & (1 << (7 - bit)):
              f.write("#")
            else:
              f.write(" ")
            bit_count += 1
            if bit_count >= width_in_pixels:
              break
        f.write("|\n")


      f.write("\n")

    f.write("};\n\n")

    f.write("// iso8859-1\n");
    f.write("extern const FontInfo " + fontStructName + " = {\n");
    f.write("  .pointSize = " + str(height_in_pixels) + ",\n");
    f.write("  .width     = " + str(width_in_pixels) + ",\n");
    f.write("  .height    = " + str(height_in_pixels) + ",\n");
    f.write("  .ascent    = " + str(font_ascent) + ",\n");
    f.write("  .inleading = 0,\n");
    f.write("  .exleading = 0,\n");
    f.write("  .flags     = 0,\n");
    f.write("  .weight    = 400,\n");
    f.write("  .charset   = 44,\n");
    f.write("  .data      = " + fontStructName + "_DATA,\n");
    f.write("  .chptr     = NULL,\n");
    f.write("  .codepage  = 1252,\n");
    f.write("};\n\n");
    f.write("#else\n\n");
    f.write("extern const FontInfo " + fontStructName + ";\n\n");
    f.write("#endif\n\n");
    f.write("} // namespace fabgl\n")

    f.close()

def print_summary():

  print("\nSummary:")
  print("\nFont info:\n")
  print("   width in pixels         = "+str(width_in_pixels))
  print("   height in pixels        = "+str(height_in_pixels))
  print("   left offset in pixels   = "+str(left_offset))
  print("   bottom offset in pixels = "+str(bottom_offset))
  print("   ascent                  = "+str(font_ascent))
  print("   descent                 = "+str(font_descent))
  print("")
  print("   width in bytes          = "+str(width_in_bytes))
  print("   height in lines         = "+str(height_in_lines))
  print("")
  print("   replacement char        = "+replacement_char)
  print("")

  print("Parsed character codes:")
  for code in parsed_codes:
    print("  ", code)
  print("")
  print("Missing character codes:")
  for ascii_code in range(0,256):
    if aggregated_bitmap_bytes[ascii_code] == []:
      print("  " + str(ascii_code) + " (" + adobe_glyph_descriptions[ascii_code] + ")")
  print("")
  print("Ascii codes with 'replacement_char' character:")
  for code in replacement_char_codes:
    print("  ", code)
  print("")
  print("Skipped character codes:")
  for code in skipped_codes:
    print("  ", code)

def print_usage(optional_error_msg = None):
  print("")
  print("bdf_to_header.py")
  print("")
  print("Convert a BDF font file to a C header-style file that will contain bitmap")
  print("data for ASCII characters 0-255.")
  print("")
  print("A log of the conversion process will be printed to the standard output and")
  print("can be redirected to a file if desired.")

  if optional_error_msg:
    print("")
    print("  *** ERROR: " + optional_error_msg)

  print("")
  print("Usage:")
  print("")
  print("  bdf_to_header.py -i <inputfile> -o <outputfile> (-r <replacementchar>) (-g <glyphdescriptionfile>)")
  print("")
  print("Example:")
  print("")
  print("  bdf_to_header.py -i ter-u14n-8x14.bdf -o ter-u14n-8x14.h > ter-u14n-8x14.log")
  print("")
  print("Options:")
  print("")
  print("  -i, --ifile")
  print("    Path to the input BDF font file to be parsed.")
  print("      This parameter is required. The script will read glyph/glyphdata from")
  print("      this file and pass it to the parser.")
  print("  -o, --ofile")
  print("    Path to the output C header-style file to be written.")
  print("      This parameter is required. The script will write the converted")
  print("      representation to this file.")
  print("  -g, --glyphdescriptions")
  print("    Path to a glyph description file used to map glyph names to ASCII character")
  print("    codes (consumed by read_charset).")
  print("      If not provided, the CP-1252 character set will be used as default.")
  print("  -r, --replacementchar")
  print("    Optional glyph name to use as the replacement for missing")
  print("    or unmapped glyphs.")
  print("      If not provided, the default Unicode replacement character 'uniFFFD' will")
  print("      be used.")
  print("      If the replacement character is not found in the input BDF file, missing")
  print("      glyphs will be rendered as a space.")
  print("  -f, --format")
  print("    Optional output format for the font data.")
  print("      Supported formats: 'structured' (default), 'fabgl'")
  print("")

def main(argv):

  global inputfile
  global outputfile
  global glyph_description_filename
  global adobe_glyph_descriptions
  global replacement_char
  global header_file_format

  startup_folder = os.path.dirname(sys.argv[0])

  try:
    opts, args = getopt.getopt(argv,"hi:o:r:g:f:",["ifile=","ofile=","replacementchar=","glyphdescriptions=","format="])
  except getopt.GetoptError:
    print_usage("Invalid command line parameters found")
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg
    elif opt in("-r", "--replacementchar"):
      replacement_char = arg
    elif opt in("-g", "--glyphdescriptions"):
      glyph_description_filename = arg
    elif opt in("-f", "--format"):
      header_file_format = arg

  if inputfile == '' or outputfile == '':
    print_usage("Input file and output file parameters are required.")
    sys.exit(2)

  print("Input file is '"+inputfile+"'")
  print("Output file is '"+outputfile+"'")
  print("Replacement character is '"+replacement_char+"'")
  print("Glyph file is '"+glyph_description_filename+"'")
  print("Header file format is '"+header_file_format+"'")

  if os.path.isfile(glyph_description_filename):
    adobe_glyph_descriptions = read_charset(glyph_description_filename)
  else:
    glyph_description_filepath = os.path.join(startup_folder, glyph_description_filename)
    if os.path.isfile(glyph_description_filepath):
      adobe_glyph_descriptions = read_charset(glyph_description_filepath)
    else:
      print_usage("\n\n--------------------------------------------------------------------------------\nGlyph description file '"+glyph_description_filename+"' not found.\n\nIt should be in the current folder or in the script startup folder:\n\n    '"+startup_folder+"'\n\nIf the file was not distributed with this script, please check the\ncomments in this script file on how to create one yourself. It's easy.\n--------------------------------------------------------------------------------")
      exit(0)

  parse_file(inputfile, outputfile)

  match header_file_format:
    case "structured":
      write_output_file_structured()
    case "fabgl":
      write_output_file_fabgl()
    case _:
      print_usage("Unknown output file format '"+header_file_format+"'. Supported formats are 'structured' and 'fabgl'.")
      exit(0)

  print_summary()


if __name__ == "__main__":
   main(sys.argv[1:])
