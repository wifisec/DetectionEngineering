#!/usr/bin/env python3
import base64, zlib
b64_encoded_utf8 = "eJwVwrENAEAIA7FVMsHvRIEEdW79Io9lZq2/RJt3AkJTBfw="
b64_encoded_utf16le = "eJw9hrEJACAQxDKKE7jTFw9a/61f3BUiISHicBnWa0XRebE/BoSmBfw="
b64_decoded_utf8 = base64.urlsafe_b64decode(b64_encoded_utf8)
b64_decoded_ut16le = base64.urlsafe_b64decode(b64_encoded_utf16le)
zlib_decompress_utf8 = zlib.decompress(b64_decoded_utf8).decode('utf-8')
zlib_decompress_utf16le = zlib.decompress(b64_decoded_ut16le).decode('utf-16le')
#Usage: UTF‑16LE is the native encoding for Windows APIs, while most Unix/Linux systems prefer UTF‑8
print(zlib_decompress_utf8)#Encoding width, variable (1-4 bytes)
print(zlib_decompress_utf16le)#.NET Framework, Fixed 2 bytes (most), 4 for surrogates, little endian
hex = "7468697320697320612074657374"
hex_to_ascii = bytes.fromhex(hex).decode('utf-8')
print(hex_to_ascii)
charcode = [84,104,105,115,32,105,115,32,97,32,116,101,115,116]
print(''.join(chr(c) for c in charcode))
#https://gchq.github.io/CyberChef/#recipe=Encode_text('UTF-8%20(65001)')Zlib_Deflate('Dynamic%20Huffman%20Coding')To_Base64('A-Za-z0-9%2B/%3D')&input=dGhpcyBpcyBhIHRlc3QuLi4uLg&oeol=CR
#https://gchq.github.io/CyberChef/#recipe=Encode_text('UTF-16LE%20(1200)')Zlib_Deflate('Dynamic%20Huffman%20Coding')To_Base64('A-Za-z0-9%2B/%3D')&input=dGhpcyBpcyBhIHRlc3QuLi4uLg&oeol=CR
#https://gchq.github.io/CyberChef/#recipe=To_Hex('None',0)&input=dGhpcyBpcyBhIHRlc3Q
#https://gchq.github.io/CyberChef/#recipe=To_Charcode('Comma',16)From_Charcode('Comma',16)&input=dGhpcyBpcyBhIHRlc3Q
