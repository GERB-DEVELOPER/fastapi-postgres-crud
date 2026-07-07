import { useState, useEffect } from 'react'
function ClienteForm({ onGuardar, clienteEditar, onCancelar }) {
  const vacio = { nombre: '', ruc: '', email: '', telefono: '' }
  const [form, setForm] = useState(clienteEditar || vacio)

  useEffect(() => {
    setForm(clienteEditar || vacio)
  }, [clienteEditar])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    onGuardar(form)
    setForm(vacio)
  }

  return (
    <form onSubmit={handleSubmit} className="card p-3 mb-4" style={{ backgroundColor: '#e8f0fe' }}>
      <h5 className="mb-3 pb-2" style={{ borderBottom: '2px solid #1565C0', color: '#1565C0' }}>
        👤 {clienteEditar ? 'Editar Cliente' : 'Nuevo Cliente'}
      </h5>
      <div className="row g-2">
        <div className="col-12">
          <label className="form-label fw-semibold">Nombre</label>
          <input
            className="form-control"
            name="nombre"
            placeholder="Ej: Ana García"
            value={form.nombre}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-12">
          <label className="form-label fw-semibold">RUC</label>
          <input
            className="form-control"
            name="ruc"
            placeholder="Ej: 20111222333"
            value={form.ruc}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-12">
          <label className="form-label fw-semibold">Email</label>
          <input
            className="form-control"
            name="email"
            placeholder="Ej: ana@mail.com"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="col-12">
          <label className="form-label fw-semibold">Teléfono</label>
          <input
            className="form-control"
            name="telefono"
            placeholder="Ej: 999888777"
            value={form.telefono}
            onChange={handleChange}
            required
          />
        </div>
      </div>
      <div className="mt-3 d-flex gap-2">
        <button type="submit" className="btn btn-success">
          {clienteEditar ? '💾 Guardar cambios' : '➕ Crear cliente'}
        </button>
        {clienteEditar && (
          <button type="button" className="btn btn-secondary" onClick={onCancelar}>
            Cancelar
          </button>
        )}
      </div>
    </form>
  )
}

export default ClienteForm