import { useState, useEffect } from 'react'

const API = 'http://localhost:8000/productos'

function Productos({ agregarLog }) {
  const [productos,       setProductos]       = useState([])
  const [productoEditar,  setProductoEditar]  = useState(null)
  const [form,            setForm]            = useState({ nombre: '', precio: '' })
  const [mostrarForm,     setMostrarForm]     = useState(false)

  useEffect(() => { cargar() }, [])

  const cargar = () => {
    fetch(`${API}/`)
      .then(r => r.json())
      .then(data => setProductos(data))
  }

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = (e) => {
    e.preventDefault()
    const url    = productoEditar ? `${API}/${productoEditar.id}` : `${API}/`
    const method = productoEditar ? 'PUT' : 'POST'
    fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre: form.nombre, precio: parseFloat(form.precio) }),
    }).then(() => {
      cargar()
      cerrarForm()
      agregarLog(productoEditar ? `Se editó el producto "${form.nombre}"` : `Se creó el producto "${form.nombre}"`)
    })
  }

  const eliminar = (id) => {
    if (!confirm('¿Eliminar este producto?')) return
    const producto = productos.find(p => p.id === id)
    fetch(`${API}/${id}`, { method: 'DELETE' }).then(() => { cargar(); agregarLog(`Se eliminó el producto "${producto?.nombre}"`) })
  }

  const abrirEditar = (p) => {
    setProductoEditar(p)
    setForm({ nombre: p.nombre, precio: p.precio })
    setMostrarForm(true)
  }

  const cerrarForm = () => {
    setProductoEditar(null)
    setForm({ nombre: '', precio: '' })
    setMostrarForm(false)
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Productos <span className="badge bg-primary">{productos.length}</span></h2>
        <button className="btn btn-danger btn-lg rounded-pill shadow-sm px-4 fw-bold" onClick={() => setMostrarForm(!mostrarForm)}>
          ➕ Nuevo producto
        </button>
      </div>

      {mostrarForm && (
        <form onSubmit={handleSubmit} className="card p-3 mb-4">
          <h5>{productoEditar ? 'Editar Producto' : 'Nuevo Producto'}</h5>
          <div className="row g-2 mt-1">
            <div className="col-md-6">
              <input className="form-control" name="nombre" placeholder="Nombre" value={form.nombre} onChange={handleChange} required />
            </div>
            <div className="col-md-6">
              <input className="form-control" name="precio" placeholder="Precio" type="number" step="0.01" value={form.precio} onChange={handleChange} required />
            </div>
          </div>
          <div className="mt-3 d-flex gap-2">
            <button type="submit" className="btn btn-primary">
              {productoEditar ? 'Guardar cambios' : 'Crear producto'}
            </button>
            <button type="button" className="btn btn-secondary" onClick={cerrarForm}>Cancelar</button>
          </div>
        </form>
      )}

      <table className="table table-striped table-hover table-bordered">
        <thead className="table-primary">
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {productos.map(p => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.nombre}</td>
              <td>S/. {parseFloat(p.precio).toFixed(2)}</td>
              <td>
                <button className="btn btn-sm btn-outline-primary me-2" onClick={() => abrirEditar(p)}>Editar</button>
                <button className="btn btn-sm btn-outline-danger" onClick={() => eliminar(p.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Productos