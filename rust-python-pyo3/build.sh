#!/bin/bash
cd rust_project
cargo build --release
cp target/release/librust_code.so ../python/rust_code.so