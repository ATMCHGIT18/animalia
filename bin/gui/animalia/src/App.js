import { useState } from "react";
import "./App.css";
import AnimalInfo from "./Components/AnimalInfo";
import SearchBar from "./Components/Search";
import WorldMap from "./Components/WorldMap";
import Footer from "./Components/Footer";
import icon from "./images/icon.png";

function App() {
  const [selected, setSelected] = useState(null);

  return (
    <div className="App">
      <div id="icon">
        <img src={icon} alt={"Animalia"}></img>
        <div>Animalia</div>
      </div>
      <div id="search">
        <SearchBar setSelected={setSelected} />
      </div>
      <div id="map">
        <WorldMap selectedData={selected} />
      </div>
      <div id="info">
        <AnimalInfo animalInfo={selected} />
      </div>
      <div id="footer">
        <Footer />
      </div>
    </div>
  );
}

export default App;
