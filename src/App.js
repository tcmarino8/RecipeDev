import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [theme, setTheme] = useState("breakfast");
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => setFile(e.target.files[0]);
  const handleThemeChange = (e) => setTheme(e.target.value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setRecipes([]);
    if (!file) {
      setError("Please upload a CSV file.");
      setLoading(false);
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    formData.append("theme", theme);

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      setRecipes(data.recipes);
    } catch (err) {
      setError("Failed to generate recipes.");
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 500, margin: "2rem auto", fontFamily: "sans-serif" }}>
      <h1>AI Recipe Generator</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>
            Upload your inventory CSV:
            <input type="file" accept=".csv" onChange={handleFileChange} required />
          </label>
        </div>
        <div>
          <label>
            Select cuisine theme:
            <select value={theme} onChange={handleThemeChange}>
              <option value="breakfast">Breakfast</option>
              <option value="bbq">BBQ</option>
              <option value="thai">Thai</option>
            </select>
          </label>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Recipes"}
        </button>
      </form>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <div style={{ marginTop: 20 }}>
        {recipes.length > 0 ? (
          <>
            <h2>Recipes you can make:</h2>
            <ul>
              {recipes.map((r, i) => (
                <li key={i}>
                  <b>{r.name}</b>: {r.ingredients.join(", ")}
                </li>
              ))}
            </ul>
          </>
        ) : null}
      </div>
    </div>
  );
}

export default App;