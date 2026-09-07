import React, { useState, useRef } from "react";

function SearchBar() {
  const [searchText, setSearchText] = useState(null);

  const getText = (event) => {};
  return (
    <div>
      <form id="searchbar">
        <input type="text" placeholder="Search..." id="searchbar-input"></input>
        <button id="searchbar-submit">
          <i className="fa fa-search"></i>
        </button>
      </form>
    </div>
  );
}

export default SearchBar;
