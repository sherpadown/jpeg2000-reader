#!/usr/bin/env python3

import sys
from bitstring import ConstBitStream


"""
	Parse & analyze only JPEG2000 compliant DCI/SMPTE file
	------------------------------------------------------
	This tool doesn't works on another JPEG2000 file
"""


# List of Markers
# with marker names and parser function names
MARKERS = {
	# Delimiting Marker Segments
	b'\xFF\x4F': {'name': "[SOC] Start of codestream", 'parser': 'default'},
	b'\xFF\x90': {'name': "[SOT] Start of tile-part", 'parser': 'sot'},
	b'\xFF\x93': {'name': "[SOD] Start of data", 'parser': 'default'},
	b'\xFF\xD9': {'name': "[EOC] End of codestream", 'parser': 'default'},
	# Fixed Information Marker Segments
	b'\xFF\x51': {'name': "[SIZ] Image and tile size", 'parser': 'siz'},
	# Functional Marker Segments
	b'\xFF\x52': {'name': "[COD] Coding style default", 'parser': 'cod'},
	b'\xFF\x53': {'name': "[COC] Coding style component", 'parser': 'default'},
	b'\xFF\x5E': {'name': "[RGN] Region-of-interest", 'parser': 'default'},
	b'\xFF\x5C': {'name': "[QCD] Quantization default", 'parser': 'qcd'},
	b'\xFF\x5D': {'name': "[QCC] Quantization component", 'parser': 'default'},
	b'\xFF\x5F': {'name': "[POC] Progression Order Change", 'parser': 'poc'},
	# Pointer Marker Segments
	b'\xFF\x55': {'name': "[TLM] Tile-part lengths, main header", 'parser': 'tlm'},
	b'\xFF\x57': {'name': "[PLM] Packet length, main header", 'parser': 'default'},
	b'\xFF\x58': {'name': "[PLT] Packet length, tile-part header", 'parser': 'default'},
	b'\xFF\x60': {'name': "[PPM] Packed packet headers, main header", 'parser': 'default'},
	b'\xFF\x61': {'name': "[PPT] Packed packet headers, tile-part header", 'parser': 'default'},
	# Bitstream Marker Segments
	b'\xFF\x91': {'name': "[SOP] Start of packet", 'parser': 'default'},
	b'\xFF\x92': {'name': "[EPH] End of packet header", 'parser': 'default'},
	# Informational Marker Segments
	b'\xFF\x64': {'name': "[CME] Comment and extension", 'parser': 'cme'},
}




# Parser for each KLV
class Parser():

	def default(data, file_handler=None):
		...

	def siz(data, file_handler=None):
		print("""---- Provides information about the uncompressed image such as the width and height of the reference grid,
---- the width and height of the tiles, the number of components, component bit depth, 
---- and the separation of component samples with respect to the reference grid""")
		bytes = ConstBitStream(data)

		rsiz = bytes.read("bits:16").uint
		print(f"SIZ - rsiz   : Profile {rsiz}")

		Xsiz = bytes.read("bits:32").uint
		Ysiz = bytes.read("bits:32").uint
		print(f"SIZ - Xsiz   : {Xsiz} px")
		print(f"SIZ - Ysiz   : {Ysiz} px")

		XOsiz = bytes.read("bits:32").uint
		YOsiz = bytes.read("bits:32").uint
		print(f"SIZ - XOsiz  : {XOsiz} px")
		print(f"SIZ - YOsiz  : {YOsiz} px")

		XTsiz = bytes.read("bits:32").uint
		YTsiz = bytes.read("bits:32").uint
		print(f"SIZ - XTsiz  : {XTsiz} px")
		print(f"SIZ - YTsiz  : {YTsiz} px")

		XTOsiz = bytes.read("bits:32").uint
		YTOsiz = bytes.read("bits:32").uint
		print(f"SIZ - XTOsiz : {XTOsiz} px")
		print(f"SIZ - YTOsiz : {YTOsiz} px")

		Csiz = bytes.read("bits:16").uint
		print(f"SIZ - Csiz   : {Csiz} components")

		# read each component parameters
		# values must be : 
		#	ssizDepth = 11
		#	xRsiz : 1
		#	yRsiz : 1
		for component in range(Csiz):
			# ssiz :
			#	x000 0000 - x010 0101 : 1 bit to 38 bits deep
			#	0xxx xxxx - components are unsigned values
			#	1xxx xxxx - components are signed values
			ssizDepth = bytes.read("bits:8")   # TODO FIXME : read only last 7 bits...
			xRsiz = bytes.read("bits:8").uint
			yRsiz = bytes.read("bits:8").uint
			print(f"SIZ - Component {component+1} - ssizDepth : {ssizDepth.uint} ─➤ {ssizDepth.uint+1} bits		Components Parameters ({ssizDepth.bin})")
			print(f"SIZ - Component {component+1} - xRsiz     : {xRsiz} bit(s)		Horizontal separation of a sample")
			print(f"SIZ - Component {component+1} - yRsiz     : {yRsiz} bit(s)		Vertical separation of a sample")


	def cod(data, file_handler=None):
		print("""---- Describes the coding style, decomposition, and layering that is
---- the default used for compressing all components of an image  or a tile""")
		bytes = ConstBitStream(data)

		# Scod
		# ------------------------------------------------------------------
		# 0000 00x0			Entropy coder, without partitions (precints)
		# 0000 00x1			Entropy coder, with partitions (precincts)
		# xxxx xx0x			No SOP marker segments used
		# xxxx xx1x			SOP marker segments may used
		# xxxx x0xx			No EPH marker segments used
		# xxxx x1xx			EPH marker segments may used
		# ------------------------------------------------------------------
		scod = bytes.read("bits:8")
		print(f"COD - Scod   : {scod.hex}					Binary Parameters: {scod.bin}")

		# ------------------------------------------------------------------
		# 0000 0000			Layer-resolution-component-position progressive
		# 0000 0001			Resolution-layer-component-position progressive
		# 0000 0010			Resolution-position-component-layer progressive
		# 0000 0011			Position-component-resolution-layer progressive
		# 0000 0100			Component-position-resolution-layer progressive
		# ------------------------------------------------------------------
		progression_order = bytes.read("bits:8")
		print(f"COD - Progression order : {progression_order.hex}				Binary Parameters: {progression_order.bin}")

		layers = bytes.read("bits:16")
		print(f"COD - Number of Layers  : {layers.int}")

		multipleComponentTransformation = bytes.read("bits:8")
		print(f"COD - Multiple Component Transform : {multipleComponentTransformation.hex} {multipleComponentTransformation.bin}")

		decompositionLevels = bytes.read("bits:8")
		print(f"COD - Decomposition levels : {decompositionLevels.uint}")

		# Code-block width and height offset exponent value
		# ---------------------------------------------------
		# codeblockSizeX = 2 ^ (valueX + 2)
		# codeblockSizeY = 2 ^ (valueY + 2)
		# ---------------------------------------------------
		codeBlockSizeXExponent = bytes.read("bits:8")
		codeBlockSizeYExponent = bytes.read("bits:8")
		codeBlockSizeX = (2 ** (codeBlockSizeXExponent.uint + 2))
		codeBlockSizeY = (2 ** (codeBlockSizeYExponent.uint + 2))
		print(f"COD - CodeBlockSize : {codeBlockSizeX} x {codeBlockSizeY}")

		# Code-block style for the SPcod and SPcoc parameters
		# ---------------------------------------------------------------------------
		# xxxx xxx0		No selective arithmetic coding bypass
		# xxxx xxx1		Selective arithmetic coding bypass
		# ---------------------------------------------------------------------------
		# xxxx xx0x		No reset of context probabilities on coding pass boundaries
		# xxxx xx1x		Reset context probabilities on coding pass boundaries
		# ---------------------------------------------------------------------------
		# xxxx x0xx		No termination on each coding pass
		# xxxx x1xx		Termination on each coding pass
		# ---------------------------------------------------------------------------
		# xxxx 0xxx		No vertically stripe causal context
		# xxxx 1xxx		Vertically stripe causal context
		# ---------------------------------------------------------------------------
		# xxx0 xxxx		No predictable termination
		# xxx1 xxxx		Predictable termination
		# ---------------------------------------------------------------------------
		# xx0x xxxx		No segmentation symbols are used
		# xx1x xxxx		Segmentation symbols are used
		# ---------------------------------------------------------------------------
		codeBlockStylesParameterBit = {
			#bitnum
			7: { 
				# 0 or 1 :)
				0: "No selective arithmetic coding bypass",
				1: "Selective arithmetic coding bypass",
			},
			6: { 
				0: "No reset of context probabilities on coding pass boundaries",
				1: "Reset context probabilities on coding pass boundaries",
			},
			5: {
				0: "No termination on each coding pass",
				1: "Termination on each coding pass",
			},
			4: {
				0: "No vertically stripe causal context",
				1: "Vertically stripe causal context",
			},
			3: {
				0: "No predictable termination",
				1: "Predictable termination",
			},
			2: {
				0: "No segmentation symbols are used",
				1: "Segmentation symbols are used",
			},
			1: {
				0: "Unknown parameter",
				1: "Unknown parameter",
			},
			0: {
				0: "Unknown parameter",
				1: "Unknown parameter",
			},
		}
		codeBlockStyle = bytes.read("bits:8")
		print(f"COD - CodeBlock style : {codeBlockStyle.bin}")
		# read each bit from codeblockStyle
		for bitnum in reversed(range(8)):
			parameterBit = codeBlockStylesParameterBit.get(bitnum).get(codeBlockStyle[bitnum])
			print(f"COD - CodeBlock style parameter bit{bitnum} : {parameterBit}")

		# Transform for the SPcod and SPcoc parameters
		transformType = bytes.read("bits:8")
		transformTypes = {
			0: "9-7 irreversible wavelet",
			1: "5-3 reversible wavelet",
		}
		print(f"COD - TransformType : {transformTypes.get(transformType.uint)} ({transformType.bin})")

		# Packet partition width and height for the SPcod parameters
		# xxxx0000 ─➤ xxxx1111		4 LSBs are the packet partition width exponent. 
		#							Only the first value may equal zero.
		# 0000xxxx —> 1111xxxx		4 MSBs are the packet partition height exponent.
		#							Only the first value may equal zero.
		for decompositionLevel in range(decompositionLevels.int+1):
			precinctSizeXExponent = bytes.read("bits:4")  # read LSB
			precinctSizeYExponent = bytes.read("bits:4")  # read MSB
			precinctSizeX = (2 ** precinctSizeXExponent.uint)
			precinctSizeY = (2 ** precinctSizeYExponent.uint)  
			print(f"COD - PrecinctSize {decompositionLevel+1} : {precinctSizeX} x {precinctSizeY}	({precinctSizeXExponent.bin}:{precinctSizeYExponent.bin})")

	"""
		Tile length marker
	"""
	def tlm(data, file_handler=None):
		print("""---- Describes the length of every tile-part in the codestream
---- Each tile-part’s length is measured from the first byte of the SOT marker segment
---- to the end of the data of that tile-part. The value of each individual tile-part length in the TLM
---- marker segment is the same as the value in the corresponding Psot in the SOT marker segment.""")

		bytes = ConstBitStream(data)

		Ztlm = bytes.read("bits:8")
		print(f"TLM - Ztlm: Index of this marker segment:", Ztlm.uint)

		# ------ Size parameters for Stlm -------------------
		# xx00 xxxx			ST = 0; Ttlm parameter is 0 bits, only one tile-part per tile, and tileparts are in index order without omission or repetition
		# xx01 xxxx			ST = 1; Ttlm parameter 8 bits
		# xx10 xxxx			ST = 2; Ttlm parameter 16 bits
		# x0xx xxxx			SP = 0; Ptlm parameter 16 bits
		# x1xx xxxx			SP = 1; Ptlm parameter 32 bits
		# ---------------------------------------------------
		Stlm = bytes.read("bits:8")
		print(f"TLM - Stlm: Size of the Ttlm and Ptlm parameters: {Stlm.bin}")

		# read bit #2
		if Stlm[1] == 1:              # x0xx xxxx
			print("TLM - Stlm Bit-Parameters: SP = 1; Ptlm parameter 32 bits")
		else:                         # x1xx xxxx
			print("TLM - Stlm Bit-Parameters: SP = 0; Ptlm parameter 16 bits")

		# read bit #3 and #4
		if Stlm[2:4].uint == 0:       # xx00 xxxx 
			print("TLM - Stlm Bit-Parameters: ST = 0; Ttlm parameter is 0 bits, only 1 tile-part per tile and tileparts are in index order without omission or repetition")
		elif Stlm[2:4].uint == 1:     # xx01 xxxx
			print("TLM - Stlm Bit-Parameters: ST = 1; Ttlm parameter 8 bits")
		elif Stlm[2:4].uint == 16:    # xx10 xxxx
			print("TLM - Stlm Bit-Parameters: ST = 2; Ttlm parameter 16 bits")

		# for JPEG2000 DCI, Ttlm = 8 bits, Ptlm = 32 bits
		# for 2K : 3
		# for 4K : 6
		for i in range(6):
			try:
				Ttlm = bytes.read("bits:8")
				Ptlm = bytes.read("bits:32")
				print(f"TLM - Ttlm -    Tile number of tile-part {i+1}: {Ttlm.uint}")
				print(f"TLM - Ptlm - Length SOT+SOD of tile-part {i+1}: {Ptlm.uint} bytes")
			except:
				...


	"""
		Progression Order Change
		Used only for 4K
		-----
		Named POC in DCI Specs
		Named POD in JPEG2000 ISO
	"""
	def poc(data, file_handler=None):
		print("---- Describes the bounds and progression order for any progression order other than default in the codestream ----")
		bytes = ConstBitStream(data)
		
		# 2 POC
		for i in ["2K", "4K"]:

			RSpoc = bytes.read("bits:8")
			print(f"POC - [{i}] RSpoc (Resolution Start) : {RSpoc.uint}\t\t({RSpoc})")

			# Length could be 8 bits or 16 bits :
			#  8 bits : if Csiz < 257
			# 16 bits : if Csiz ≥ 257
			CSpoc = bytes.read("bits:8")  # Csiz < 257, so 8 bits
			print(f"POC - [{i}] CSpoc (Component Start)  : {CSpoc.uint}\t\t({CSpoc})")

			LYEpoc = bytes.read("bits:16")
			print(f"POC - [{i}] LYEpoc (Layer)           : {LYEpoc.uint}\t\t({LYEpoc})")

			REpoc = bytes.read("bits:8")
			print(f"POC - [{i}] REpoc (Resolution End)   : {REpoc.uint}\t\t({REpoc})")

			# Length could be 8 bits or 16 bits :
			#  8 bits : if Csiz < 257
			# 16 bits : if Csiz ≥ 257
			CEpoc = bytes.read("bits:8")  # Csiz < 257, so 8 bits
			print(f"POC - [{i}] CEpoc (Component End)    : {CEpoc.uint}\t\t({CEpoc})")

			Ppoc = bytes.read("bits:8")
			print(f"POC - [{i}] Ppoc (Progression Order) : {Ppoc.uint}\t\t({Ppoc})")



	def sot(data, file_handler=None):
		print("""---- Marks the beginning of a tile-part and the index of its tile within a codestream
---- The tile-parts of a tile shall appear in order (see TPsot) in the codestream
---- but not necessarily consecutively.""")
		bytes = ConstBitStream(data)

		Isot = bytes.read("bits:16")
		print("SOT - Isot, Tile number           :", Isot.uint)

		Psot = bytes.read("bits:32")
		print("SOT - Psot, Length of SOT+SOD     :", Psot.uint)

		TPsot = bytes.read("bits:8")
		print("SOT - TPsot, Tile-part number     :", TPsot.uint)

		TNsot = bytes.read("bits:8")
		print("SOT - TNsot, Number of tile-parts :", TNsot.uint)

		# use Psot length, minus header to calculate SOD_length
		SOD_length = Psot.uint - 12
		# read SOD data, remove marker of SOD
		SOD_data = file_handler.read(SOD_length)[2:]
		
		p = Parser()
		p.sod(SOD_data, file_handler)

	"""
		Start of Data
		start_of_data is not a KLV, we have not length, only raw data
		Start of Data is linked to SOT.
		To determine length of SOD, read TLM or SOT
	"""
	def sod(self, data, file_handler=None):
		marker = b'\xff\x93'
		marker_name = MARKERS.get(marker).get('name')
		print(f"\n{marker_name:45s} ({marker.hex().upper()})")
		print(f"data: {len(data)} bytes : {data.hex()}")


	"""
		Comment and extension Marker
	"""
	def cme(bytes, file_handler=None):
		print("---- Comment, extension and unstructured data in the header")
		bytes = ConstBitStream(data)

		Rcme = bytes.read("bits:16")
		print(f"CME - Registration values {Rcme.uint}", end=': ')
		if Rcme.uint == 0:
			print(f"Binary values")
		if Rcme.uint == 1:
			print(f"Text ISO 8859-1")
		if Rcme.uint > 1:
			print(f"Reserved")

		# ------------------------------------------------
		# 0        = General use (binary values)
		# 1        = General use (ISO 8859-1 (latin-1)
		# 2—>65534 = Reserved for registration
		# 65535    = Reserved for extension
		# ------------------------------------------------
		if Rcme.uint == 1:
			length = int(len(bytes) - bytes.pos)
			text = bytes.read(f"bits:{length}")
			text = text.tobytes().decode('iso-8859-1')
			print(f"CME - Text: {text}")


	def qcd(data, file_handler=None):
		print("""---- Describes the quantization default used for compressing all components not defined by a QCC marker segment.
---- The parameter values can be overridden for an individual component by a QCC marker segment in either the main or tile-part header""")
		bytes = ConstBitStream(data)

		Sqcd = bytes.read("bits:8")
		print(f"QCD - Sqcd (Scalar coefficient dequantization), Quantization style for all components: {Sqcd.bin}")
		print(f"QCD - Sqcd binary parameters (bit1-3): Number of guard bits 0—7: {Sqcd[0:3]} ─➤ {Sqcd[0:3].uint} bits")

		if Sqcd[3:8].bin == "00010":
			print(f"QCD - Sqcd: {Sqcd[3:8]} ─➤ Scalar explicit")
		else:
			print(f"QCD - Sqcd: {Sqcd[3:8]} ─➤ Scalar NOT explicit (wrong bits)")

		# Quantization values for scalar quantization for the SPqcd and SPqcc parameters - for 9-7 transform
		# Mantissa is 16 bits for 9-7
		# xxxxx00000000000 — xxxxx11111111111		Mantissa of the quantization step size value
		# 00000xxxxxxxxxxx — 11111xxxxxxxxxxx		Exponent of the quantization step size value
		for i in range(60):
			try:
				SPqcd = bytes.read("bits:16")
				mantissa = SPqcd[0:5]
				exponent = SPqcd[5:16]
				print(f"QCD - SPqcd (Exponent+Mantissa), Quantization step size value sub-band {i:-2d}:")
				print(f"\t─➤ SPqcd    : {SPqcd.bin}  (0x{SPqcd.hex})")
				print(f"\t─➤ Mantissa : {mantissa.bin:<16s} : {mantissa.uint}")
				print(f"\t─➤ Exponent : {exponent.bin:>16s} : {exponent.uint}")
			except:
				...
	

#-------------------------------------------------
#
#						Main
#
#-------------------------------------------------


for filename in sys.argv[1:]:

	print(f"read {filename}")

	# Read file and parse each KLV
	with open(filename, "rb") as file:

		while True:

			position = file.tell()

			marker = file.read(2)
			if not marker:
				break

			# [SOC] Start of codestream
			if marker == b'\xFF\x4F':
				# we have no data
				length = 0
				data = b''

			# [EOC] End of codestream (end-of-file)
			elif marker == b'\xFF\xD9':
				# we have no data
				length = 0
				data = b''

			# All others KLV
			else:
				length = int.from_bytes(file.read(2), byteorder='big')
				length -= 2				# remove marker from length
				if length < 0:			# avoid negative number
					length = 0
				data = file.read(length)

			# check if marker is there
			if not MARKERS.get(marker):
				print(f"undefined marker {marker.hex()}")
				continue

			# get name of this marker
			marker_name = MARKERS.get(marker).get('name')
			# get parser of this marker
			marker_parser_name = MARKERS.get(marker).get('parser')
			# get function parse into Parser() class
			marker_parser = getattr(
				Parser,               # class Parser
				marker_parser_name,   # method in class Parser
				Parser.default        # default class
			)

			print(f"{marker_name:45s} ({marker.hex().upper()})")

			if data:
				print(f"offs: {position}")
				print(f"size: {length} bytes")
				print(f"data: {len(data)} bytes readed: {data.hex()}")
				marker_parser(data, file)
				print(f"\n")
