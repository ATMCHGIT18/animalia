import { useState } from "react";
import "./App.css";
import AnimalInfo from "./Components/AnimalInfo";
import SearchBar from "./Components/Search";
import WorldMap from "./Components/WorldMap";
import Footer from "./Components/Footer";
import icon from "./images/icon.png";

function App() {
  const [animalInfo, setAnimalInfo] = useState(null);
  const [selectedAnimal, setSelectedAnimal] = useState(null);

  return (
    <div className="App">
      <div id="icon">
        <img src={icon}></img>
        <div>Animalia</div>
      </div>
      <div id="search">
        <SearchBar />
      </div>
      <div id="map">
        <WorldMap
          setAnimalInfo={setAnimalInfo}
          setSelectedAnimal={setSelectedAnimal}
        />
      </div>
      <div id="info">
        <AnimalInfo animalInfo={animalInfo} />
      </div>
      <div id="footer">
        <Footer />
      </div>
    </div>
  );
}

export default App;
