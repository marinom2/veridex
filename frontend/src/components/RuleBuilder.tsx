import React, { useEffect, useState } from "react";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";

interface FieldDef {
  name: string;
  label: string;
  type: "string" | "number" | "date";
  options?: string[];
}

interface RuleBlock {
  id: string;
  field: string;
  operator: string;
  value: string;
}

interface RuleGroup {
  id: string;
  logic: "AND" | "OR";
  children: (RuleBlock | RuleGroup)[];
}

const operatorMap: Record<FieldDef["type"], string[]> = {
  string: ["EQ", "NEQ", "IN"],
  number: ["EQ", "NEQ", "GT", "LT"],
  date: ["EQ", "NEQ", "BEFORE", "AFTER"],
};

export const RuleBuilder: React.FC = () => {
  const [fields, setFields] = useState<FieldDef[]>([]);
  const [rootGroup, setRootGroup] = useState<RuleGroup>({
    id: uuidv4(),
    logic: "AND",
    children: [],
  });

  useEffect(() => {
    async function fetchInitialData() {
      try {
        const fieldRes = await axios.get("/fields");
        setFields(fieldRes.data);

        const rulesRes = await axios.get("/rules/load");
        if (rulesRes.data?.rules) {
          setRootGroup(rulesRes.data.rules);
        }
      } catch (err) {
        console.error("Failed to fetch initial data", err);
        alert("❌ Failed to load initial field or rule data");
      }
    }

    fetchInitialData();
  }, []);

  const addRule = (groupId: string) => {
    const newRule: RuleBlock = {
      id: uuidv4(),
      field: "",
      operator: "",
      value: "",
    };
    setRootGroup((prev) => insertIntoGroup(prev, groupId, newRule));
  };

  const addGroup = (groupId: string) => {
    const newGroup: RuleGroup = {
      id: uuidv4(),
      logic: "AND",
      children: [],
    };
    setRootGroup((prev) => insertIntoGroup(prev, groupId, newGroup));
  };

  const deleteGroup = (group: RuleGroup, groupId: string): RuleGroup => {
    return {
      ...group,
      children: group.children
        .map((child) => {
          if ("children" in child) {
            if (child.id === groupId) return null;
            return deleteGroup(child, groupId);
          }
          return child;
        })
        .filter(Boolean) as (RuleGroup | RuleBlock)[],
    };
  };

  const insertIntoGroup = (
    group: RuleGroup,
    targetId: string,
    newChild: RuleBlock | RuleGroup
  ): RuleGroup => {
    if (group.id === targetId) {
      return { ...group, children: [...group.children, newChild] };
    }
    return {
      ...group,
      children: group.children.map((child) =>
        "children" in child ? insertIntoGroup(child, targetId, newChild) : child
      ),
    };
  };

  const updateGroupLogic = (
    group: RuleGroup,
    groupId: string,
    logic: "AND" | "OR"
  ): RuleGroup => {
    if (group.id === groupId) return { ...group, logic };
    return {
      ...group,
      children: group.children.map((child) =>
        "children" in child ? updateGroupLogic(child, groupId, logic) : child
      ),
    };
  };

  const updateRule = (
    group: RuleGroup,
    ruleId: string,
    key: keyof RuleBlock,
    val: string
  ): RuleGroup => {
    return {
      ...group,
      children: group.children.map((child) => {
        if ("children" in child) return updateRule(child, ruleId, key, val);
        if (child.id === ruleId) return { ...child, [key]: val };
        return child;
      }),
    };
  };

  const deleteRule = (group: RuleGroup, ruleId: string): RuleGroup => {
    return {
      ...group,
      children: group.children
        .map((child) =>
          "children" in child ? deleteRule(child, ruleId) : child
        )
        .filter((child) => "id" in child && child.id !== ruleId),
    };
  };

  const formatValue = (field: FieldDef | undefined, value: string): string => {
    if (!field) return `'${value}'`;
    if (field.type === "number") return value;
    if (field.type === "date") return `'${value}'`;
    return `'${value.replace(/'/g, "''")}'`;
  };

  const getSQL = (group: RuleGroup): string => {
    const clauses = group.children.map((child) => {
      if ("children" in child) return `(${getSQL(child)})`;
      const field = fields.find((f) => f.name === child.field);
      return `${child.field} ${child.operator} ${formatValue(field, child.value)}`;
    });
    return clauses.join(` ${group.logic} `);
  };

  const saveRulesAndSQL = async () => {
    const sql = getSQL(rootGroup);
    try {
      await axios.post("/rules/save", {
        rules: rootGroup,
        sql,
      });
      alert("✅ Rules and SQL saved.");
    } catch (err) {
      console.error("Error saving rules", err);
      alert("❌ Failed to save.");
    }
  };

  const renderRule = (rule: RuleBlock) => {
    const field = fields.find((f) => f.name === rule.field);
    const operators = field ? operatorMap[field.type] || [] : [];

    return (
      <div key={rule.id} className="flex gap-2 items-center">
        <select
          value={rule.field}
          onChange={(e) =>
            setRootGroup((prev) =>
              updateRule(prev, rule.id, "field", e.target.value)
            )
          }
          className="border p-1 rounded"
        >
          <option value="">Select field</option>
          {fields.map((f) => (
            <option key={f.name} value={f.name}>
              {f.label}
            </option>
          ))}
        </select>

        <select
          value={rule.operator}
          onChange={(e) =>
            setRootGroup((prev) =>
              updateRule(prev, rule.id, "operator", e.target.value)
            )
          }
          className="border p-1 rounded"
        >
          <option value="">Op</option>
          {operators.map((op) => (
            <option key={op} value={op}>
              {op}
            </option>
          ))}
        </select>

        <input
          type="text"
          value={rule.value}
          onChange={(e) =>
            setRootGroup((prev) =>
              updateRule(prev, rule.id, "value", e.target.value)
            )
          }
          className="border p-1 rounded"
          placeholder="Value"
        />

        <button
          onClick={() =>
            setRootGroup((prev) => deleteRule(prev, rule.id))
          }
          className="text-red-500"
        >
          ❌
        </button>
      </div>
    );
  };

  const renderGroup = (group: RuleGroup) => (
    <div key={group.id} className="border-l-2 pl-4 my-4">
      <div className="flex items-center gap-2 mb-2">
        <label className="font-bold">Logic:</label>
        <select
          value={group.logic}
          onChange={(e) =>
            setRootGroup((prev) =>
              updateGroupLogic(prev, group.id, e.target.value as "AND" | "OR")
            )
          }
          className="border p-1 rounded"
        >
          <option value="AND">AND</option>
          <option value="OR">OR</option>
        </select>
        <button
          onClick={() => addRule(group.id)}
          className="bg-blue-500 text-white px-2 py-1 rounded"
        >
          ➕ Rule
        </button>
        <button
          onClick={() => addGroup(group.id)}
          className="bg-green-500 text-white px-2 py-1 rounded"
        >
          ➕ Group
        </button>
        {group.id !== rootGroup.id && (
          <button
            onClick={() =>
              setRootGroup((prev) => deleteGroup(prev, group.id))
            }
            className="text-red-500 ml-auto"
          >
            🗑️ Delete Group
          </button>
        )}
      </div>

      <div className="ml-4 space-y-2">
        {group.children.map((child) =>
          "children" in child ? renderGroup(child) : renderRule(child)
        )}
      </div>
    </div>
  );

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">🔀 Visual Rule Logic</h1>
      {renderGroup(rootGroup)}

      <div className="mt-6">
        <h3 className="font-semibold">🧮 SQL Preview:</h3>
        <pre className="bg-gray-100 p-4 rounded text-sm">
          {getSQL(rootGroup) || "-- No rules defined --"}
        </pre>
        <button
          onClick={saveRulesAndSQL}
          className="mt-4 bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          💾 Save Rules & SQL
        </button>
      </div>
    </div>
  );
};