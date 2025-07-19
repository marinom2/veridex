// src/App.tsx
import React from 'react';
import './App.css';
import { RuleBuilder } from './components/RuleBuilder';  // ✅ match the actual export name

function App() {
  return (
    <div className="App p-6">
      <h1 className="text-2xl font-bold mb-4">🧠 Veridex Rule Builder</h1>
      <RuleBuilder />
    </div>
  );
}

export default App;