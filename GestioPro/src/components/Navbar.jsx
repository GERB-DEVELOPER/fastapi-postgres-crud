import { NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'

function Navbar() {
  const [hora, setHora] = useState(new Date())

  useEffect(() => {
    const timer = setInterval(() => setHora(new Date()), 1000)
    return () => clearInterval(timer)
  }, [])

  const linkStyle = (isActive) => ({
    fontSize: '1.2rem',
    color: isActive ? '#69f0ae' : '#fff',
    borderBottom: isActive ? '2px solid #69f0ae' : '2px solid transparent',
    paddingBottom: '2px',
  })

  const links = [
    { to: '/inicio',    label: '🏠 Inicio'    },
    { to: '/clientes',  label: '🧑 Clientes'  },
    { to: '/productos', label: '📦 Productos' },
    { to: '/ventas',    label: '🧾 Ventas'    },
    { to: '/logger',    label: '📋 Historial'  },
  ]

  return (
    <nav className="navbar navbar-expand-lg navbar-dark px-4 mb-4 shadow" style={{ backgroundColor: '#1a237e' }}>
      <NavLink to="/inicio" className="navbar-brand fw-bold d-flex align-items-center gap-2">
        <img src="/logogerb.png" alt="logo" style={{ height: '90px', width: 'auto' }} />
        GestioPro
      </NavLink>
      <button
        className="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navMenu"
      >
        <span className="navbar-toggler-icon"></span>
      </button>
      <div className="collapse navbar-collapse" id="navMenu">
        <div className="navbar-nav ms-3">
          {links.map(link => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => 'nav-link' + (isActive ? ' fw-bold' : '')}
              style={({ isActive }) => linkStyle(isActive)}
            >
              {link.label}
            </NavLink>
          ))}
        </div>
        <div className="ms-auto text-white small text-end">
          <div style={{ fontWeight: 600 }}>Sistema de Gestión</div>
          <div style={{ color: '#90caf9', fontSize: '0.85rem' }}>
            {hora.toLocaleTimeString('es-PE')} — {hora.toLocaleDateString('es-PE')}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar