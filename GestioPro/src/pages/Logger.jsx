function Logger({ logs, onLimpiar }) {
  return (
    <div>
      <div className="d-flex align-items-center gap-3 mb-4">
        <h2 className="mb-0">📋 Historial de Actividad</h2>
        <span className="badge bg-primary fs-6">{logs.length} registros</span>
        {logs.length > 0 && (
          <button className="btn btn-outline-danger btn-sm ms-auto" onClick={onLimpiar}>
            🗑️ Limpiar historial
          </button>
        )}
      </div>

      {logs.length === 0 ? (
        <div className="text-center text-muted py-5">
          <div style={{ fontSize: '3rem' }}>📭</div>
          <p className="mt-2">No hay actividad registrada aún.</p>
        </div>
      ) : (
        <table className="table table-striped table-hover table-bordered">
          <thead className="table-dark">
            <tr>
              <th style={{ width: '60px' }}>Estado</th>
              <th style={{ width: '130px' }}>Fecha</th>
              <th style={{ width: '130px' }}>Hora</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id}>
                <td className="text-center">
                  {log.tipo === 'exito' ? '✅' : '❌'}
                </td>
                <td>{log.fecha}</td>
                <td>{log.hora}</td>
                <td>{log.mensaje}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default Logger
