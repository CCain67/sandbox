# Rust Project with Python Bindings

This is a (very) simple piece of rust code with bindings to python provided by `pyo3`. To build the project, just run
```bash
bash build.sh
```
while in the root directory. This will build the rust project, and move the `.so` file to a directory where you can find it and import it into a notebook (for example). 