# Python Fallback Implementations

This directory contains Python fallback implementations for various cryptographic algorithms used in the AlgoVault project. These implementations are used when the corresponding C++/Java executables are not available or encounter errors.

## Directory Structure

- `caesar/`: Caesar Cipher implementation
- `vigenere/`: Vigenere Cipher implementation
- `hill/`: Hill Cipher implementation
- `des/`: DES (Data Encryption Standard) implementation
- `sha512/`: SHA-512 hash function implementation

Each subdirectory contains:
- `__init__.py`: Makes the directory a proper Python package and exports the main function
- `*_fallback.py`: Contains the implementation of the algorithm

## Usage

These fallback implementations are imported and used in `views.py` when needed:

```python
from .python_fallback.caesar import caesar_cipher_fallback
from .python_fallback.vigenere import vigenere_cipher_fallback
from .python_fallback.hill import hill_cipher_fallback
from .python_fallback.des import des_fallback
from .python_fallback.sha512 import sha512_hash
```

## Project Structure

The overall project structure is:

```
Algorithms/
  ├── cpp_source/           # C++ source code for algorithms
  │   ├── caesar_cipher.cpp
  │   ├── vigenere_processor.cpp
  │   └── hill_processor.cpp
  ├── python_fallback/      # Python fallback implementations
  │   ├── caesar/
  │   ├── vigenere/
  │   ├── hill/
  │   ├── des/
  │   └── sha512/
  ├── *.exe                 # Compiled executables from cpp_source
  └── views.py              # Django views that use the implementations
```

When the `compile.sh` script is run, it compiles the C++ source files from the `cpp_source` directory and places the executables in the main Algorithms directory. The Django views try to use these executables first, and fall back to the Python implementations if they're not available or encounter errors.

## Implementation Notes

- The implementations match the specifications from the PDF documentation
- Each implementation includes error handling and proper documentation
- For DES, a simplified implementation is provided as a placeholder
- For SHA-512, Python's built-in hashlib library is used

## Web Interface Links

When running the Django development server (usually on port 8001), you can access the web interfaces at:

- Home page: [http://127.0.0.1:8001/](http://127.0.0.1:8001/)
- Caesar Cipher: [http://127.0.0.1:8001/caesar/](http://127.0.0.1:8001/caesar/)
- Vigenere Cipher: [http://127.0.0.1:8001/vigenere/](http://127.0.0.1:8001/vigenere/)
- Hill Cipher: [http://127.0.0.1:8001/hill/](http://127.0.0.1:8001/hill/)
- DES: [http://127.0.0.1:8001/des/](http://127.0.0.1:8001/des/)
- SHA-512: [http://127.0.0.1:8001/sha512/](http://127.0.0.1:8001/sha512/)

To start the server on port 8001, run:
```bash
python3 manage.py runserver 8001
```

## Maintenance

When updating the C++/Java implementations, make sure to update the corresponding Python fallback implementations to maintain consistency in behavior.

