import React, { useEffect, useState } from 'react';
import api from '../api';

interface Field {
  name: string;
  type: 'string' | 'number' | 'date';
  description?: string;
}

export const FieldEditor: React.FC = () => {
  const [fields, setFields] = useState<Field[]>([]);
  const [newField, setNewField] = useState<Field>({ name: '', type: 'string' });

  useEffect(() => {
    loadFields();
  }, []);

  const loadFields = async () => {
    try {
      const res = await api.get('/fields');
      const data = res.data.fields || res.data;
      setFields(data);
    } catch (err) {
      console.error('❌ Failed to load fields:', err);
      alert('❌ Error loading field definitions');
    }
  };

  const addField = async () => {
    if (!newField.name.trim() || !newField.type) {
      alert('⚠️ Please fill out both name and type');
      return;
    }

    try {
      await api.post('/fields', newField);
      setNewField({ name: '', type: 'string' });
      loadFields();
    } catch (err) {
      console.error('❌ Error adding field:', err);
      alert('❌ Failed to add field. Field name might already exist.');
    }
  };

  const deleteField = async (name: string) => {
    if (!window.confirm(`Are you sure you want to delete "${name}"?`)) return;

    try {
      await api.delete(`/fields/${name}`);
      loadFields();
    } catch (err) {
      console.error('❌ Error deleting field:', err);
      alert('❌ Failed to delete field');
    }
  };

  return (
    <div className="p-4 border rounded-xl shadow bg-white">
      <h2 className="text-xl font-bold mb-4">🧱 Define Fields</h2>

      <div className="mb-6 flex gap-2 flex-wrap items-center">
        <input
          type="text"
          placeholder="Field name"
          value={newField.name}
          onChange={(e) => setNewField({ ...newField, name: e.target.value })}
          className="border p-2 rounded w-40"
        />
        <select
          value={newField.type}
          onChange={(e) => setNewField({ ...newField, type: e.target.value as Field['type'] })}
          className="border p-2 rounded w-32"
        >
          <option value="">Type</option>
          <option value="string">string</option>
          <option value="number">number</option>
          <option value="date">date</option>
        </select>
        <button
          onClick={addField}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          ➕ Add Field
        </button>
      </div>

      <ul className="space-y-2">
        {fields.map((field) => (
          <li
            key={field.name}
            className="flex justify-between items-center border p-2 rounded bg-gray-50"
          >
            <span>
              <strong>{field.name}</strong> ({field.type})
            </span>
            <button
              onClick={() => deleteField(field.name)}
              className="text-red-600 hover:underline"
            >
              ✖ Remove
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};