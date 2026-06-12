"""Convert a flat binary to UF2 for the Raspberry Pi Pico 2 W (RP2350 ARM-S)."""
import struct, sys, pathlib

FLASH_BASE     = 0x10000000  # RP2350 XIP flash start
UF2_MAGIC0     = 0x0A324655
UF2_MAGIC1     = 0x9E5D5157
UF2_MAGIC_END  = 0x0AB16F30
FAMILY_ID      = 0xe48bff59  # RP2350_ARM_S
BLOCK_DATA     = 256          # payload bytes per block
FLAG_FAMILY_ID = 0x00002000   # flags field: familyID present

def convert(bin_path: str, uf2_path: str) -> None:
    data = pathlib.Path(bin_path).read_bytes()
    # pad to multiple of 256
    if len(data) % BLOCK_DATA:
        data += b'\x00' * (BLOCK_DATA - len(data) % BLOCK_DATA)
    blocks = len(data) // BLOCK_DATA
    out = bytearray()
    for i in range(blocks):
        chunk = data[i * BLOCK_DATA : (i + 1) * BLOCK_DATA]
        addr  = FLASH_BASE + i * BLOCK_DATA
        # UF2 block: 32 bytes header + 476 bytes payload (256 data + 220 zeroes) + 4 bytes magic end
        hdr = struct.pack('<IIIIIIII',
                          UF2_MAGIC0,
                          UF2_MAGIC1,
                          FLAG_FAMILY_ID,
                          addr,
                          BLOCK_DATA,
                          i,
                          blocks,
                          FAMILY_ID)
        payload = chunk + b'\x00' * (476 - BLOCK_DATA)
        out += hdr + payload + struct.pack('<I', UF2_MAGIC_END)
    pathlib.Path(uf2_path).write_bytes(out)
    print(f"Wrote {blocks} blocks -> {uf2_path}")

if __name__ == "__main__":
    bin_path = sys.argv[1] if len(sys.argv) > 1 else "HW3.bin"
    uf2_path = sys.argv[2] if len(sys.argv) > 2 else bin_path.replace(".bin", ".uf2")
    convert(bin_path, uf2_path)
