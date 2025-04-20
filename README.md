# JPEG2000 Reader

JPEG2000-reader analyzes and explains J2C DCI (Digital Cinema) format


## Usage


### Installation 

```
$ uv venv
$ source .venv/bin/activate
$ uv sync
```

#### Using

```
$ python -m jpeg2000_reader <filename>
```

Example :

```
$ python -m jpeg2000_reader tests/assets/black_2k.j2c | grep '^\['
[SOC] Start of codestream                     (FF4F)
[SIZ] Image and tile size                     (FF51)
[COD] Coding style default                    (FF52)
[QCD] Quantization default                    (FF5C)
[TLM] Tile-part lengths, main header          (FF55)
[SOT] Start of tile-part                      (FF90)
[SOD] Start of data                           (FF93)
[SOT] Start of tile-part                      (FF90)
[SOD] Start of data                           (FF93)
[SOT] Start of tile-part                      (FF90)
[SOD] Start of data                           (FF93)
[EOC] End of codestream                       (FFD9)


$ python -m jpeg2000_reader tests/assets/black_2k.j2c
read tests/assets/black_2k.j2c
[SOC] Start of codestream                     (FF4F)
[SIZ] Image and tile size                     (FF51)
offs: 2
size: 45 bytes
data: 45 bytes readed: 0003000008000000043800000000000000000000080000000438000000000000000000030b01010b01010b0101
---- Provides information about the uncompressed image such as the width and height of the reference grid,
---- the width and height of the tiles, the number of components, component bit depth,
---- and the separation of component samples with respect to the reference grid
SIZ - rsiz   : Profile 3
SIZ - Xsiz   : 2048 px
SIZ - Ysiz   : 1080 px
SIZ - XOsiz  : 0 px
SIZ - YOsiz  : 0 px
SIZ - XTsiz  : 2048 px
SIZ - YTsiz  : 1080 px
SIZ - XTOsiz : 0 px
SIZ - YTOsiz : 0 px
SIZ - Csiz   : 3 components
SIZ - Component 1 - ssizDepth : 11 ─➤ 12 bits           Components Parameters (00001011)
SIZ - Component 1 - xRsiz     : 1 bit(s)                Horizontal separation of a sample
SIZ - Component 1 - yRsiz     : 1 bit(s)                Vertical separation of a sample
SIZ - Component 2 - ssizDepth : 11 ─➤ 12 bits           Components Parameters (00001011)
SIZ - Component 2 - xRsiz     : 1 bit(s)                Horizontal separation of a sample
SIZ - Component 2 - yRsiz     : 1 bit(s)                Vertical separation of a sample
SIZ - Component 3 - ssizDepth : 11 ─➤ 12 bits           Components Parameters (00001011)
SIZ - Component 3 - xRsiz     : 1 bit(s)                Horizontal separation of a sample
SIZ - Component 3 - yRsiz     : 1 bit(s)                Vertical separation of a sample


[COD] Coding style default                    (FF52)
offs: 51
size: 16 bytes
data: 16 bytes readed: 01040001010503030000778888888888
---- Describes the coding style, decomposition, and layering that is
---- the default used for compressing all components of an image  or a tile
COD - Scod   : 01                                       Binary Parameters: 00000001
COD - Progression order : 04                            Binary Parameters: 00000100


(.... stripped // not the full output content ....)


[SOD] Start of data                           (FF93)
data: 59 bytes : 8080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080


[SOT] Start of tile-part                      (FF90)
offs: 455
size: 8 bytes
data: 8 bytes readed: 0000000000490203
---- Marks the beginning of a tile-part and the index of its tile within a codestream
---- The tile-parts of a tile shall appear in order (see TPsot) in the codestream
---- but not necessarily consecutively.
SOT - Isot, Tile number           : 0
SOT - Psot, Length of SOT+SOD     : 73
SOT - TPsot, Tile-part number     : 2
SOT - TNsot, Number of tile-parts : 3

[SOD] Start of data                           (FF93)
data: 59 bytes : 8080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080


[EOC] End of codestream                       (FFD9)
```

