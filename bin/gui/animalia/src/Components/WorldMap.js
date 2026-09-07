import React, { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import { loadAnimal } from "./Utils";

import "maplibre-gl/dist/maplibre-gl.css";

import lion from "../data/animals/lion.json";
import polarBear from "../data/animals/polar_bear.json";
import AnimalInfo from "./AnimalInfo";

maplibregl.setWorkerUrl("/maplibre-gl-worker.mjs");

function WorldMap({ setAnimalInfo, setSelectedAnimal }) {
  const mapContainer = useRef(null);
  const mapRef = useRef(null);

  /*
   * Create the MapLibre map.
   */

  useEffect(() => {
    if (mapRef.current) {
      return;
    }

    const map = new maplibregl.Map({
      container: mapContainer.current,

      style: "/styles/map_source.json",

      center: [0, 20],

      zoom: 1.4,
    });

    // For testing that if there is an error or not

    map.on("load", () => {
      console.log("MAP LOADED");

      console.log("test source:", map.getSource("test-polygon"));

      console.log("test fill:", map.getLayer("test-polygon-fill"));

      console.log("test outline:", map.getLayer("test-polygon-outline"));
    });

    map.on("error", (event) => {
      console.error("MAPLIBRE ERROR:", event);
    });

    map.addControl(new maplibregl.NavigationControl(), "top-right");

    mapRef.current = map;

    /*
     * Cleanup when React removes the component.
     */

    return () => {
      map.remove();

      mapRef.current = null;
    };
  }, []);

  const clickHandle = () => {
    loadAnimal(lion, mapRef, setSelectedAnimal, setAnimalInfo);
  };

  return (
    <div
      style={{
        width: "100%",
        height: "100vh",
        position: "relative",
      }}
    >
      <div
        ref={mapContainer}
        style={{
          width: "100%",
          height: "100%",
        }}
      />
      <button onClick={clickHandle}>Lions</button>
    </div>
  );
}

export default WorldMap;
