import { useState, useEffect } from 'react'

const API_VENTAS    = 'http://localhost:8000/ventas'
const API_CLIENTES  = 'http://localhost:8000/clientes'
const API_PRODUCTOS = 'http://localhost:8000/productos'

function Ventas({ agregarLog }) {
  const [ventas,       setVentas]       = useState([])
  const [clientes,     setClientes]     = useState([])
  const [productos,    setProductos]    = useState([])
  const [mostrarForm,  setMostrarForm]  = useState(false)
  const [form,         setForm]         = useState({
    cliente_id: '', producto_id: '', cantidad: '', fecha: '', total: ''
  })

  useEffect(() => {
    cargarVentas()
    fetch(`${API_CLIENTES}/`).then(r => r.json()).then(setClientes)
    fetch(`${API_PRODUCTOS}/`).then(r => r.json()).then(setProductos)
  }, [])

  const cargarVentas = () => {
    fetch(`${API_VENTAS}/`).then(r => r.json()).then(setVentas)
  }

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = (e) => {
    e.preventDefault()
    fetch(`${API_VENTAS}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        cliente_id:  parseInt(form.cliente_id),
        producto_id: parseInt(form.producto_id),
        cantidad:    parseInt(form.cantidad),
        fecha:       form.fecha,
        total:       parseFloat(form.total),
      }),
    }).then(() => {
      cargarVentas()
      cerrarForm()
      agregarLog(`Se registró una venta por S/. ${parseFloat(form.total).toFixed(2)}`)
    })
  }

  const eliminar = (id) => {
    if (!confirm('¿Eliminar esta venta?')) return
    fetch(`${API_VENTAS}/${id}`, { method: 'DELETE' }).then(() => { cargarVentas(); agregarLog(`Se eliminó la venta #${id}`) })
  }

  const cerrarForm = () => {
    setForm({ cliente_id: '', producto_id: '', cantidad: '', fecha: '', total: '' })
    setMostrarForm(false)
  }

  const nombreCliente  = (id) => clientes.find(c => c.id === id)?.nombre  || id
  const nombreProducto = (id) => productos.find(p => p.id === id)?.nombre || id

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2>Ventas <span className="badge bg-primary">{ventas.length}</span></h2>
        <button className="btn btn-danger btn-lg rounded-pill shadow-sm px-4 fw-bold" onClick={() => setMostrarForm(!mostrarForm)}>
          ➕ Nueva venta
        </button>
      </div>

      {mostrarForm && (
        <form onSubmit={handleSubmit} className="card p-3 mb-4">
          <h5>Nueva Venta</h5>
          <div className="row g-2 mt-1">
            <div className="col-md-6">
              <select className="form-select" name="cliente_id" value={form.cliente_id} onChange={handleChange} required>
                <option value="">-- Seleccionar cliente --</option>
                {clientes.map(c => <option key={c.id} value={c.id}>{c.nombre}</option>)}
              </select>
            </div>
            <div className="col-md-6">
              <select className="form-select" name="producto_id" value={form.producto_id} onChange={handleChange} required>
                <option value="">-- Seleccionar producto --</option>
                {productos.map(p => <option key={p.id} value={p.id}>{p.nombre} — S/. {p.precio}</option>)}
              </select>
            </div>
            <div className="col-md-4">
              <input className="form-control" name="cantidad" placeholder="Cantidad" type="number" value={form.cantidad} onChange={handleChange} required />
            </div>
            <div className="col-md-4">
              <input className="form-control" name="fecha" placeholder="Fecha" type="datetime-local" value={form.fecha} onChange={handleChange} required />
            </div>
            <div className="col-md-4">
              <input className="form-control" name="total" placeholder="Total" type="number" step="0.01" value={form.total} onChange={handleChange} required />
            </div>
          </div>
          <div className="mt-3 d-flex gap-2">
            <button type="submit" className="btn btn-primary">Registrar venta</button>
            <button type="button" className="btn btn-secondary" onClick={cerrarForm}>Cancelar</button>
          </div>
        </form>
      )}

      <table className="table table-striped table-hover table-bordered">
        <thead className="table-primary">
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Producto</th>
            <th>Cantidad</th>
            <th>Fecha</th>
            <th>Total</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {ventas.map(v => (
            <tr key={v.id}>
              <td>{v.id}</td>
              <td>{nombreCliente(v.cliente_id)}</td>
              <td>{nombreProducto(v.producto_id)}</td>
              <td>{v.cantidad}</td>
              <td>{v.fecha}</td>
              <td>S/. {parseFloat(v.total).toFixed(2)}</td>
              <td>
                <button className="btn btn-sm btn-outline-danger" onClick={() => eliminar(v.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Ventas