import React from "react";
import "./search_item.css";

function SearchItem({ page, onClick, key }) {
  return (
    <div key={key} className="search-result-result" onClick={onClick}>
      <img
        src={
          page.thumbnail.url.startsWith("//")
            ? `https:${page.thumbnail.url}`
            : page.thumbnail.url
        }
        alt={page.title}
        className="search-result-image"
        style={{
          width: page.thumbnail.width,
          height: page.thumbnail.height,
        }}
      />
      <div>
        <h4 style={{ margin: "0 0 5px 0" }}>
          <a
            href={`https://en.wikipedia.org/wiki/${page.key}`}
            target="_blank"
            rel="noreferrer"
            style={{ color: "#0066cc", textDecoration: "none" }}
          >
            {page.title}
          </a>
        </h4>
        <p className="search-result-result-description">
          {page.description || "No description available"}
        </p>
        {/* Using dangerouslySetInnerHTML because Wikipedia excerpts contain HTML search match tags (<span class="searchmatch">) */}
        <p
          style={{
            margin: 0,
            fontSize: "13px",
            color: "#666",
            lineHeight: "1.4",
          }}
          dangerouslySetInnerHTML={{ __html: page.excerpt || "" }}
        />
      </div>
    </div>
  );
}

export default SearchItem;
