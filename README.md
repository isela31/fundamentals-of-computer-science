# Fundamentals of Computer Science — Coursework (2021)

> Selected assignments completed in **Nov 2021** as part of the course **“Fundamentals of Computer Science”**.  
> Uploaded for reference and to demonstrate foundational programming + algorithmic thinking (Python).

This repository contains **selected** homework solutions:
- **Work 4:** Convolutional encoder + Viterbi-style hard-decision decoder (trellis + Hamming-distance path metrics)
- **Work 3:** A custom `String` class implementing encoding/transformation utilities (Base64, byte-pair encoding, cyclic transforms, histogram)

---

## 📁 Contents

### עבודה 4 — Convolutional Code + Decoder (`convolutional_code.py`)
Implements a convolutional coding system with:
- **k = 1** input bit per step
- **Zero-tail termination** (encoder ends in all-zero state)
- Encoder defined by **generator polynomials** (integers)
- **Hard-decision decoding** using a trellis over `2^L` states
- Path metric computed via **Hamming distance**
- Returns `(decoded_bytes, distance)`

**Key classes**
- `ConvolutionalCode`: `encode(data: bytes) -> List[int]`, `decode(bits: List[int]) -> (bytes, int)`
- `State`: precomputes transitions/output for input bit 0/1
- `Path`: stores path word + accumulated distance

**Generator convention**
The code uses the convention described in comments:
`1 + D = b011 = 3` (LSB corresponds to lower-order terms).

---

### עבודה 3 — String Encodings Toolkit (`String.py`)
A custom `String` class that supports:
- `base64()` — Base64 encoding (custom implementation)
- `byte_pair_encoding()` — Byte-Pair Encoding with generated replacement rules
- `cyclic_bits(num)` — cyclic rotation on the **bit level** across the entire string
- `cyclic_chars(num)` — cyclic shift of printable ASCII characters (wraps within 32..126)
- `histogram_of_chars()` — character histogram into bins (digits/upper/lower/other/etc.)

Includes custom exceptions:
- `Base64DecodeError`, `CyclicCharsError`, `BytePairError`, `BytePairDecodeError`

---

## ▶️ How to run (quick sanity checks)

### Work 4 (Convolutional Code)
```python
from convolutional_code import ConvolutionalCode

# Example generator polynomials (as integers)
cc = ConvolutionalCode(generators=(7, 5))

data = b"hello"
encoded = cc.encode(data)                 # -> list of bits (0/1)
decoded, dist = cc.decode(encoded)        # -> (bytes, int)

print(decoded, dist)
