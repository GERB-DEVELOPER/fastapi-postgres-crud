function ClienteCard({ cliente, ventasCount, onEditar, onEliminar }) {
  const colores = [
    { fondo: '#e3f2fd', borde: '#1565C0', avatar: '#1565C0' },
    { fondo: '#e8f5e9', borde: '#2E7D32', avatar: '#2E7D32' },
    { fondo: '#fff3e0', borde: '#E65100', avatar: '#E65100' },
    { fondo: '#f3e5f5', borde: '#6A1B9A', avatar: '#6A1B9A' },
    { fondo: '#e0f7fa', borde: '#00838F', avatar: '#00838F' },
  ]
  const color   = colores[cliente.id % colores.length]
  const inicial = cliente.nombre.charAt(0).toUpperCase()

  return (
    <div
      className="card shadow-sm h-100"
      style={{
        backgroundColor: color.fondo,
        borderTop:    '1px solid rgba(0,0,0,0.08)',
        borderRight:  '1px solid rgba(0,0,0,0.08)',
        borderBottom: '1px solid rgba(0,0,0,0.08)',
        borderLeft:   `5px solid ${color.borde}`,
      }}
    >
      <div className="card-body p-2">
        <div className="d-flex align-items-center gap-2 mb-2">
          <div style={{
            width: '40px', height: '40px', borderRadius: '50%',
            backgroundColor: color.avatar, color: '#fff',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '1.1rem', fontWeight: 800, flexShrink: 0,
          }}>
            {inicial}
          </div>
          <div style={{ minWidth: 0 }}>
            <div className="fw-bold" style={{ color: color.borde, fontSize: '0.95rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {cliente.nombre}
            </div>
            <span className="badge" style={{ backgroundColor: color.borde, fontSize: '0.7rem' }}>
              🧾 {ventasCount} ventas
            </span>
          </div>
        </div>
        <div style={{ fontSize: '0.8rem' }}>
          <div className="mb-1">📧 {cliente.email}</div>
          <div className="mb-1">📞 {cliente.telefono}</div>
          <div><span className="badge bg-secondary" style={{ fontSize: '0.7rem' }}>RUC: {cliente.ruc}</span></div>
        </div>
      </div>
      <div className="card-footer d-flex gap-1 p-2" style={{ backgroundColor: 'transparent', border: 'none' }}>
        <button className="btn btn-sm btn-primary flex-fill" onClick={() => onEditar(cliente)}>
          ✏️ Editar
        </button>
        <button className="btn btn-sm btn-danger flex-fill" onClick={() => onEliminar(cliente.id)}>
          🗑️ Eliminar
        </button>
      </div>
    </div>
  )
}

export default ClienteCard
