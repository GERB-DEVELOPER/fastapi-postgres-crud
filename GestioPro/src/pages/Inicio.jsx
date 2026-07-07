import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

function Inicio() {
  const [totalClientes,  setTotalClientes]  = useState(0)
  const [totalProductos, setTotalProductos] = useState(0)
  const [totalVentas,    setTotalVentas]    = useState(0)
  const [montoTotal,     setMontoTotal]     = useState(0)

  useEffect(() => {
    fetch('http://localhost:8000/clientes/')
      .then(r => r.json())
      .then(data => setTotalClientes(data.length))

    fetch('http://localhost:8000/productos/')
      .then(r => r.json())
      .then(data => setTotalProductos(data.length))

    fetch('http://localhost:8000/ventas/')
      .then(r => r.json())
      .then(data => {
        setTotalVentas(data.length)
        const monto = data.reduce((acc, v) => acc + parseFloat(v.total), 0)
        setMontoTotal(monto)
      })
  }, [])

  const stats = [
    { titulo: 'Clientes',  valor: totalClientes,                  bg: '#1565C0', ruta: '/clientes',  col: 'col-md-3' },
    { titulo: 'Productos', valor: totalProductos,                 bg: '#2E7D32', ruta: '/productos', col: 'col-md-3' },
    { titulo: 'Ventas',    valor: totalVentas,                    bg: '#E65100', ruta: '/ventas',    col: 'col-md-2' },
    { titulo: 'Ingresos',  valor: `S/. ${montoTotal.toFixed(2)}`, bg: '#6A1B9A', ruta: '/ventas',    col: 'col-md-4' },
  ]

  return (
    <div>
      <h1 className="page-title">Panel de Control</h1>

      <div className="row g-4 mb-5">
        {stats.map(stat => (
          <div className={stat.col} key={stat.titulo}>
            <Link to={stat.ruta} style={{ textDecoration: 'none' }}>
              <div className="card stat-card" style={{ background: stat.bg, border: 'none' }}>
                <div className="card-body p-4">
                  <p style={{ color: 'rgba(255,255,255,0.85)', fontSize: '1rem', marginBottom: '0.5rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '1px' }}>
                    {stat.titulo}
                  </p>
                  <div style={{ color: '#fff', fontSize: '2.8rem', fontWeight: 800, lineHeight: 1 }}>
                    {stat.valor}
                  </div>
                </div>
              </div>
            </Link>
          </div>
        ))}
      </div>

      <h5 className="text-muted mb-3">Acceso rápido</h5>
      <div className="d-flex gap-3">
        <Link to="/clientes"  className="btn btn-primary px-4">Ver Clientes</Link>
        <Link to="/productos" className="btn btn-success px-4">Ver Productos</Link>
        <Link to="/ventas"    className="btn btn-warning px-4">Ver Ventas</Link>
      </div>
    </div>
  )
}

export default Inicio