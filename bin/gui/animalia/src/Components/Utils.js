export async function loadAnimal(
  animal,
  mapRef,
  setSelectedAnimal,
  setAnimalInfo,
) {
  if (!mapRef.current) {
    return;
  }

  try {
    /*
     * Fetch the geographic range.
     */

    const response = await fetch(animal.distribution.range_file);

    if (!response.ok) {
      throw new Error(`Could not load range for ${animal.common_name}`);
    }

    const range = await response.json();

    /*
     * Add map styling information
     * to the GeoJSON features.
     */

    range.features = range.features.map((feature) => ({
      ...feature,

      properties: {
        ...feature.properties,

        fill_color: animal.map.fill_color,

        fill_opacity: animal.map.fill_opacity,

        outline_color: animal.map.outline_color,
      },
    }));

    /*
     * Get the existing source
     * from style.json.
     */

    const source = mapRef.current.getSource("animal-range");

    if (!source) {
      console.error("animal-range source was not found.");

      return;
    }

    /*
     * Replace the source data.
     */

    source.setData(range);
    /*
     * Update React state.
     */

    setSelectedAnimal(animal.id);

    setAnimalInfo(animal);
  } catch (error) {
    console.error("Animal loading error:", error);
  }
}
