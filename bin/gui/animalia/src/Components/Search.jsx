import React, { useState } from "react";
import "./search.css";
import SearchResultContainer from "./SearchResultContainer";

function SearchBar({ setSelected, setAnimalInfo }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const selectItem = async (selectedPage) => {
    console.log(selectedPage);
    setSelected(selectedPage);
    setData(null);

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        "http://localhost:8000/api/create_selected_animal",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ selectedAnimal: selectedPage }),
        },
      );

      if (!response.ok) {
        throw new Error(
          "Something went wrong on creating the selected animal data",
        );
      }

      const jsonResult = await response.json();
      setAnimalInfo(jsonResult);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setData(null);

    try {
      const response = await fetch("http://localhost:8000/api/search-animals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query }),
      });

      if (!response.ok) {
        throw new Error("Something went wrong with the server calculation.");
      }

      const jsonResult = await response.json();
      setData(jsonResult);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div id="search-div">
      <form id="searchbar" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search..."
          id="searchbar-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        ></input>
        <button type="submit" disabled={loading} id="searchbar-submit">
          <i className="fa fa-search"></i>
        </button>
      </form>
      {/* Show the result  */}
      {error && <p style={{ color: "red" }}>Error: {error}</p>}
      {data && <SearchResultContainer data={data} selectItem={selectItem} />}
    </div>
  );
}

export default SearchBar;
