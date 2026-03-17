import React, { useEffect } from 'react'
import { StreamlitProvider } from 'streamlit-component-lib-react-hooks'
import PosApp from './PosApp'

function App() {
  return (
    <StreamlitProvider>
      <PosApp />
    </StreamlitProvider>
  )
}

export default App
