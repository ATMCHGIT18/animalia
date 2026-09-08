import React, { useState } from "react";
import "./search_result_container.css";
import SearchItem from "./SearchItem";

function SearchResultContainer({ data, selectItem }) {
  return (
    <div id="search-result">
      <span>
        Results for: "<i>{data.query}</i>"
      </span>
      <div id="search-result-main-div">
        {data.results.map((page) => {
          return (
            <SearchItem
              page={page}
              onClick={() => selectItem(page)}
              key={page.id}
            />
          );
        })}
      </div>
    </div>
  );
}

export default SearchResultContainer;
