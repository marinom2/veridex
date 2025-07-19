
import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Field {
  name: string;
  type: string;
  description?: string;
}

export const FieldEditor: React.FC = () => {
  const [fields, setFields] = useState<Field[]>([]);
  const [newField, setNewField] = useState<Field>({ name: '', type: '' });

  useEffect(() => {
    loadFields();
  }, []);

  const loadFields = async () => {
    const res = await axios.get('/fields');
    setFields(res.data.fields);
  };

  const addField = async () => {
    await axios.post('/fields', newField);
    setNewField({ name: '', type: '' });
    loadFields();
  };

  const deleteField = async (name: string) => {
    await axios.delete(`/fields/${name}`);
    loadFields();
  };

  return (
    <div className="p-4 border rounded-xl">
      <h2 className="text-xl font-bold mb-2">🧱 Define Fields</h2>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Field name"
          value={newField.name}
          onChange={(e) => setNewField({ ...newField, name: e.target.value })}
          className="border p-2 mr-2 rounded"
        />
        <select
          value={newField.type}
          onChange={(e) => setNewField({ ...newField, type: e.target.value })}
          className="border p-2 rounded"
        >
          <option value="">Type</option>
          <option value="string">string</option>
          <option value="number">number</option>
          <option value="date">date</option>
        </select>
        <button onClick={addField} className="ml-2 px-4 py-2 bg-blue-600 text-white rounded">
          ➕ Add Field
        </button>
      </div>

      <ul className="space-y-2">
        {fields.map((field) => (
          <li key={field.name} className="flex justify-between border p-2 rounded">
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

