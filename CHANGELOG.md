# Changelog v0.12.2

## Improvements

* **Module Encapsulation**
  Added `__all__` declarations to module files to explicitly define public exports and improve internal package structure.
  Commits: [b09c04a](https://github.com/aurumorinc/koda/commit/b09c04a8), [18ccb03](https://github.com/aurumorinc/koda/commit/18ccb03a)

* **Script Execution Safety**
  Implemented conditional execution blocks (`if __name__ == "__main__":`) within the recording script to prevent unintended execution when the module is imported.
  Commits: [b09c04a](https://github.com/aurumorinc/koda/commit/b09c04a8), [18ccb03](https://github.com/aurumorinc/koda/commit/18ccb03a)
