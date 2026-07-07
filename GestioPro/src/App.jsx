import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState } from 'react'
import Navbar    from './components/Navbar'
import Inicio    from './pages/Inicio'
import Clientes  from './pages/Clientes'
import Productos from './pages/Productos'
import Ventas    from './pages/Ventas'
import Logger    from './pages/Logger'

function App() {
  const [logs, setLogs] = useState(() => {
    const guardados = localStorage.getItem('gestiopro_logs')
    return guardados ? JSON.parse(guardados) : []
  })

  const agregarLog = (mensaje, tipo = 'exito') => {
    const nuevoLog = {
      id:      Date.now(),
      hora:    new Date().toLocaleTimeString('es-PE'),
      fecha:   new Date().toLocaleDateString('es-PE'),
      mensaje,
      tipo,
    }
    setLogs(prev => {
      const actualizados = [nuevoLog, ...prev]
      localStorage.setItem('gestiopro_logs', JSON.stringify(actualizados))
      return actualizados
    })
  }

  const limpiarLogs = () => {
    setLogs([])
    localStorage.removeItem('gestiopro_logs')
  }

  return (
    <BrowserRouter>
      <Navbar />
      <div className="container-fluid px-4 pb-5">
        <Routes>
          <Route path="/"          element={<Navigate to="/inicio" />} />
          <Route path="/inicio"    element={<Inicio />} />
          <Route path="/clientes"  element={<Clientes  agregarLog={agregarLog} />} />
          <Route path="/productos" element={<Productos agregarLog={agregarLog} />} />
          <Route path="/ventas"    element={<Ventas    agregarLog={agregarLog} />} />
          <Route path="/logger"    element={<Logger logs={logs} onLimpiar={limpiarLogs} />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
