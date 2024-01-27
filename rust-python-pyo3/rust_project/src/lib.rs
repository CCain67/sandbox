use pyo3::prelude::*;

#[pyfunction]
fn add(a: i32, b: i32) -> PyResult<i32> {
    Ok(a + b)
}

#[pymodule]
fn rust_code(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}
