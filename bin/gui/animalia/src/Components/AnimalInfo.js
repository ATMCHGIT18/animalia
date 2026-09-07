import React, { useEffect, useRef, useState } from "react";

/* This component will be updated by adding the new info to the animal's JSON files */

function AnimalInfo({ animalInfo }) {
  return (
    animalInfo && (
      <div id="animalinfo-container">
        <img
          id="animalinfo-image"
          src={animalInfo.imageurl}
          alt={animalInfo.common_name + "-" + animalInfo.scientific_name}
        ></img>
        <h2 id="animalinfo-name">{animalInfo.common_name}</h2>

        <p id="animalinfo-sciname">
          <i>{animalInfo.scientific_name}</i>
        </p>

        <p id="animalinfo-conservation">
          <strong>Conservation:</strong>{" "}
          <span
            style={{
              backgroundColor:
                animalInfo.conservation.status === "Vulnerable"
                  ? "orange"
                  : animalInfo.conservation.status === "Extinct"
                    ? "red"
                    : animalInfo.conservation.status === "Near Threat"
                      ? "yellow"
                      : "transparent",
            }}
          >
            {animalInfo.conservation.status}
          </span>
        </p>

        <p id="animalinfo-habitat">
          <strong>Habitat:</strong>
        </p>

        <ul id="animalinfo-habitats">
          {animalInfo.habitat.map((habitat) => (
            <li key={habitat}>{habitat}</li>
          ))}
        </ul>

        <div id="animalinfo-physical">
          {Object.keys(animalInfo.physical.data).length > 2
            ? Object.keys(animalInfo.physical.data).map((key) => (
                <div>
                  <label key={animalInfo.physical.data[key]}>
                    {key.toString().replace("_", " ") + " : "}
                  </label>

                  <span key={animalInfo.physical.data[key]}>
                    {animalInfo.physical.data[key].min +
                      " - " +
                      animalInfo.physical.data[key].max}
                  </span>
                </div>
              ))
            : ""}
        </div>
      </div>
    )
  );
}

export default AnimalInfo;
