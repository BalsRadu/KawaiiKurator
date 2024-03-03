import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [showFilters, setShowFilters] = useState(false);
  const [filterSelections, setFilterSelections] = useState({
    popularity: '',
    score: '',
    type: '',
    episodes: '',
    source: '',
  });
  const [isGenreSelected, setIsGenreSelected] = useState(false);
  const [jsonData, setJsonData] = useState(Array.from({ length: 5 }, (_, i) => ({
    image_anime_url: '',
    synopsis: '',
    genre: '',
    english_title: '',
    score: ''
  })));
  const [imagesLoaded, setImagesLoaded] = useState(false);

  const toggleFilters = () => setShowFilters(!showFilters);

  const handleFilterChange = (filter, value) => {
    setFilterSelections({ ...filterSelections, [filter]: value });
  };

  const handleGenreCheckboxChange = (e) => {
    setIsGenreSelected(e.target.checked);
  };

  // Log the current state to the console whenever it changes
  useEffect(() => {
    console.log(filterSelections);
    console.log(`Is Genre Selected: ${isGenreSelected}`);
  }, [filterSelections, isGenreSelected]);

    // Function to generate JSON objects and update the jsonData state
    const generateAndSetJsonData = () => {
      const generatedData = Array.from({ length: 5 }, (_, i) => ({
        image_anime_url: `https://th.bing.com/th/id/R.cd3a3b71f7ec78684d9217a0f3471a94?rik=QqQCfaUEhG3hqA&riu=http%3a%2f%2fwallup.net%2fwp-content%2fuploads%2f2016%2f12%2f08%2f409898-puppies-dog.jpg&ehk=d5HxI3ueB3zY3O10UKUYpn5qtt%2bxUe6c8v1Db44RNWU%3d&risl=&pid=ImgRaw&r=0`,
        synopsis: `Synopsis ${i + 1}`,
        genre: isGenreSelected ? `Genre ${i + 1}` : 'N/A',
        english_title: `English Title ${i + 1}`,
        score: `Score ${i + 1}`
      }));
      setJsonData(generatedData);
      handleLoadImages(); // Call to control image loading
    };
  
    // Function to control the loading of images
    const handleLoadImages = () => {
      setImagesLoaded(true);
    };

  return (
    <div className="app">
      <div className="banner">Banner</div>
      <div className="controls">
        <div className="input-group">
          <input type="text" placeholder="Enter user" />
          <button onClick={generateAndSetJsonData}>Go User</button>
        </div>
        <div className="input-group">
          <input type="text" placeholder="Enter anime" />
          <button onClick={generateAndSetJsonData}>Go Anime</button>
        </div>
        <div className="genre-checkbox">
          <input
            type="checkbox"
            id="genreCheckbox"
            checked={isGenreSelected}
            onChange={handleGenreCheckboxChange}
          />
          <label htmlFor="genreCheckbox">Genre</label>
        </div>
        <div className="filter-button">
          <button onClick={toggleFilters}>Filter</button>
        </div>
        {showFilters && (
          <div className="filter-dropdowns">
            <div className="row">
              <div>
                <div>Popularity</div>
                <select value={filterSelections.popularity} onChange={(e) => handleFilterChange('popularity', e.target.value)}>
                  <option value="popularity1">Popularity 1</option>
                  <option value="popularity2">Popularity 2</option>
                  <option value="popularity3">Popularity 3</option>
                  <option value="popularity4">Popularity 4</option>
                  <option value="popularity5">Popularity 5</option>
                </select>
              </div>
              <div>
                <div>Score</div>
                <select value={filterSelections.score} onChange={(e) => handleFilterChange('score', e.target.value)}>
                  <option value="score1">Score 1</option>
                  <option value="score2">Score 2</option>
                  <option value="score3">Score 3</option>
                  <option value="score4">Score 4</option>
                  <option value="score5">Score 5</option>
                </select>
              </div>
              <div>
                <div>Type</div>
                <select value={filterSelections.type} onChange={(e) => handleFilterChange('type', e.target.value)}>
                  <option value="type1">Type 1</option>
                  <option value="type2">Type 2</option>
                  <option value="type3">Type 3</option>
                  <option value="type4">Type 4</option>
                  <option value="type5">Type 5</option>
                </select>
              </div>
            </div>
            <div className="row">
              <div>
                <div># Episodes</div>
                <select value={filterSelections.episodes} onChange={(e) => handleFilterChange('episodes', e.target.value)}>
                  <option value="episodes1"># Episodes 1</option>
                  <option value="episodes2"># Episodes 2</option>
                  <option value="episodes3"># Episodes 3</option>
                  <option value="episodes4"># Episodes 4</option>
                  <option value="episodes5"># Episodes 5</option>
                </select>
              </div>
              <div>
                <div>Source</div>
                <select value={filterSelections.source} onChange={(e) => handleFilterChange('source', e.target.value)}>
                  <option value="source1">Source 1</option>
                  <option value="source2">Source 2</option>
                  <option value="source3">Source 3</option>
                  <option value="source4">Source 4</option>
                  <option value="source5">Source 5</option>
                </select>
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="content">
  {jsonData.map((data, index) => (
    <div key={index} className="container">
      {imagesLoaded && <img src={data.image_anime_url} alt={`Anime ${index + 1}`} style={{ maxWidth: '100%', height: 'auto' }} />}      <p>{data.english_title}</p>
      <p>{data.genre}</p>
      <p>{data.score}</p>
      <p className="synopsis">{data.synopsis}</p> {/* Use class name for targeting */}
    </div>
  ))}
</div>
      <div className="info-text">This is some static information text in the fourth element.</div>
    </div>
  );
}

export default App;
