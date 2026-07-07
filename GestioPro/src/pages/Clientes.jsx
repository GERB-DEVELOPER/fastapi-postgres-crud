import { useState, useEffect } from 'react'
import ClienteCard from '../components/ClienteCard'
import ClienteForm from '../components/ClienteForm'

//const API = 'http://localhost:8000/clientes'
const API = 'https://fastapi-postgres-crud.onrender.com/clientes'


function Clientes({ agregarLog }) {
  const [clientes,      setClientes]      = useState([])
  const [ventas,        setVentas]        = useState([])
  const [cargando,      setCargando]      = useState(true)
  const [clienteEditar, setClienteEditar] = useState(null)
  const [busqueda,      setBusqueda]      = useState('')

  useEffect(() => {
    cargarClientes()
    //fetch('http://localhost:8000/ventas/').then(r => r.json()).then(setVentas)

  fetch('https://fastapi-postgres-crud.onrender.com/ventas/').then(r => r.json()).then(setVentas)


  }, [])

  const cargarClientes = () => {
    setCargando(true)
    fetch(`${API}/`)
      .then(res => res.json())
      .then(data => { setClientes(data); setCargando(false) })
  }

  const crearCliente = (form) => {
    fetch(`${API}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    }).then(() => { cargarClientes(); agregarLog(`Se creó el cliente "${form.nombre}"`) })
  }

  const editarCliente = (form) => {
    fetch(`${API}/${clienteEditar.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    }).then(() => { setClienteEditar(null); cargarClientes(); agregarLog(`Se editó el cliente "${form.nombre}"`) })
  }

  const eliminarCliente = (id) => {
    if (!confirm('¿Eliminar este cliente?')) return
    const cliente = clientes.find(c => c.id === id)
    fetch(`${API}/${id}`, { method: 'DELETE' }).then(() => { cargarClientes(); agregarLog(`Se eliminó el cliente "${cliente?.nombre}"`) })
  }

  const onGuardar = (form) => {
    if (clienteEditar) editarCliente(form)
    else crearCliente(form)
  }

  const ventasDeCliente = (id) => ventas.filter(v => v.cliente_id === id).length

  const clientesFiltrados = clientes.filter(c =>
    c.nombre.toLowerCase().includes(busqueda.toLowerCase())
  )

  if (cargando) return <p>Cargando...</p>

  return (
    <div>
      <div className="d-flex align-items-center gap-3 mb-3">
        <h2 className="mb-0">Clientes</h2>
        <span className="badge bg-primary fs-6">{clientes.length} registrados</span>
      </div>

      <div className="row g-4">
        <div className="col-md-3">
          <ClienteForm
            onGuardar={onGuardar}
            clienteEditar={clienteEditar}
            onCancelar={() => setClienteEditar(null)}
          />
        </div>
        <div className="col-md-9">
          <input
            className="form-control mb-3"
            placeholder="🔍 Buscar cliente por nombre..."
            value={busqueda}
            onChange={e => setBusqueda(e.target.value)}
          />
          <div className="row g-3">
            {clientesFiltrados.map(c => (
              <div className="col-md-3" key={c.id}>
                <ClienteCard
                  cliente={c}
                  ventasCount={ventasDeCliente(c.id)}
                  onEditar={setClienteEditar}
                  onEliminar={eliminarCliente}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Clientes
