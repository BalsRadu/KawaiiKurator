import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const initialFilterSelections = {
    popularity: '',
    score: '',
    episodes: '',
    genre: '',
  };
  const [showFilters, setShowFilters] = useState(false);
  const [filterSelections, setFilterSelections] = useState(initialFilterSelections);
  const [isGenreSelected, setIsGenreSelected] = useState(false);
  const [jsonData, setJsonData] = useState(Array.from({ length: 5 }, (_, i) => ({
    image_anime_url: '',
    synopsis: '',
    genre: '',
    english_title: '',
    score: ''
  })));
  const [imagesLoaded, setImagesLoaded] = useState(false);
  const [animeName, setAnimeName] = useState('');
  const [username, setUsername] = useState('');

  const toggleFilters = () => setShowFilters(!showFilters);

  const handleFilterChange = (filter, value) => {
    setFilterSelections({ ...filterSelections, [filter]: value });
  };

  const clearFilters = () => {
    setFilterSelections(initialFilterSelections);
  };
  

  const handleGenreCheckboxChange = (e) => {
    setIsGenreSelected(e.target.checked);
  };

  // Log the current state to the console whenever it changes
  useEffect(() => {
    console.log(filterSelections);
    console.log(`Is Genre Selected: ${isGenreSelected}`);
  }, [filterSelections, isGenreSelected]);

  // Function to control the loading of images
  const handleLoadImages = () => {
    setImagesLoaded(true);
  };

  // Function to generate JSON objects and update the jsonData state for the unchecked anime
  const generateAndSetJsonDataAnimeName = (responseData) => {
    const generatedData = responseData.map((anime) => ({
      image_anime_url: anime['Image URL'],
      synopsis: anime.Synopsis,
      genre: anime.Genres,
      english_title: anime.Name,
      score: `Score: ${anime.Score} Similarity: ${anime.Similarity}`
    }));
    setJsonData(generatedData);
    handleLoadImages(); // Call to control image loading
  };

  const generateAndSetJsonDataAnimeTitle = (responseData) => {
    const generatedData = responseData.map((anime) => ({
      image_anime_url: anime['Image URL'],
      synopsis: anime.Synopsis,
      genre: anime.Genres,
      english_title: anime.Name,
      score: `Score: ${anime.Score}`
    }));
    setJsonData(generatedData);
    handleLoadImages(); // Call to control image loading
  };

  const handleGoAnimeNameAndTitle = async () => {
    // Ensure that animeName is not empty
    if (!animeName.trim()) {
      console.error('Anime name is required');
      return;
    }
    
    // Encode the animeName to safely include it in the URL
    const encodedAnimeName = encodeURIComponent(animeName);
    const encodedPopularity = encodeURIComponent(filterSelections.popularity);
    const encodedScore = encodeURIComponent(filterSelections.score);
    const encodedEpisodes = encodeURIComponent(filterSelections.episodes);
    const encodedGenre = encodeURIComponent(filterSelections.genre);
    
    // Construct the URL with the query parameter
    // Determine the URL based on whether the genre checkbox is selected
  const baseUrl = 'https://0609-2a02-2f09-3d0d-3300-1527-47fe-ad2b-94fd.ngrok-free.app/recommendations/';
  var url = isGenreSelected
    ? `${baseUrl}content?anime_title=${encodedAnimeName}`
    : `${baseUrl}anime?anime_name=${encodedAnimeName}`;
  if (filterSelections.popularity !== '') {
    url += `&popularity=${encodedPopularity}`;
  }
  if(filterSelections.score !== ''){
    url += `&score=${encodedScore}`;
  }
  if(filterSelections.episodes !== ''){
    url += `&episodes=${encodedEpisodes}`;
  }
  if(filterSelections.genre !== ''){
    url += `&genre=${encodedGenre}`;
  }  
    try {
      const response = await fetch(url, {
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
        }),
      })
      const data = await response.json();
      console.log('Recommendations:', data); // Log the response data to the console
      // Call the appropriate function based on isGenreSelected
      if (isGenreSelected) {
        generateAndSetJsonDataAnimeTitle(data); // If genre checkbox is selected
      } else {
        generateAndSetJsonDataAnimeName(data); // If genre checkbox is not selected
      }
      } catch (error) {
        console.error('There was an error fetching anime recommendations:', error);
    }
  };

  // Function to generate JSON objects and update the jsonData state for the username
  const generateAndSetJsonDataUsername = (responseData) => {
    const generatedData = responseData.map((anime) => ({
      image_anime_url: anime['Image URL'],
      synopsis: anime.Synopsis,
      genre: anime.Genres,
      english_title: anime.Name,
      score: `Score: ${anime.Score} Total Preferences: ${anime['Total Preferences']}`
    }));
    setJsonData(generatedData);
    handleLoadImages(); // Call to control image loading
  };

  const handleGoUsername = async () => {
    // Ensure that animeName is not empty
    if (!username.trim()) {
      console.error('Username is required');
      return;
    }
    
    // Encode the animeName to safely include it in the URL
    const encodedUserName = encodeURIComponent(username);
    const encodedPopularity = encodeURIComponent(filterSelections.popularity);
    const encodedScore = encodeURIComponent(filterSelections.score);
    const encodedEpisodes = encodeURIComponent(filterSelections.episodes);
    const encodedGenre = encodeURIComponent(filterSelections.genre);
    
    // Construct the URL with the query parameter
    var url = `https://0609-2a02-2f09-3d0d-3300-1527-47fe-ad2b-94fd.ngrok-free.app/recommendations/user?username=${encodedUserName}`;
    if (filterSelections.popularity !== '') {
      url += `&popularity=${encodedPopularity}`;
    }
    if(filterSelections.score !== ''){
      url += `&score=${encodedScore}`;
    }
    if(filterSelections.episodes !== ''){
      url += `&episodes=${encodedEpisodes}`;
    }
    if(filterSelections.genre !== ''){
      url += `&genre=${encodedGenre}`;
    } 
    
    try {
      const response = await fetch(url, {
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
        }),
      })
      const data = await response.json();
      console.log('Recommendations:', data); // Log the response data to the console
      // Call generateAndSetJsonData with the fetched data
      generateAndSetJsonDataUsername(data);
      } catch (error) {
        console.error('There was an error fetching anime recommendations:', error);
      }
  };

  return (
    <div className="app">
      <div className="banner">Welcome to the Quiz</div>
      <div className="controls">
        <div className="input-group">
          <input type="text" placeholder="Enter user" value={username}
            onChange={(e) => setUsername(e.target.value)}/>
          <button onClick={handleGoUsername}>Go User</button>
        </div>
        <div className="input-group">
          <input type="text" placeholder="Enter anime" value={animeName}
            onChange={(e) => setAnimeName(e.target.value)}/>
          <button onClick={handleGoAnimeNameAndTitle}>Go Anime</button>
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
              <button onClick={clearFilters}>Clear</button>
            </div>
            <div className="row">
              <div>
              <div>Popularity</div>
                <input 
                  type="text" 
                  value={filterSelections.popularity} 
                  onChange={(e) => handleFilterChange('popularity', e.target.value)} 
                  placeholder="Enter Popularity"
                />
              </div>
              <div>
              <div>Score</div>
                <input 
                  type="text" 
                  value={filterSelections.score} 
                  onChange={(e) => handleFilterChange('score', e.target.value)} 
                  placeholder="Enter Score"
                />
              </div>
            </div>
            <div className="row">
              <div>
                <div># Episodes</div>
                  <input 
                    type="text" 
                    value={filterSelections.episodes} 
                    onChange={(e) => handleFilterChange('episodes', e.target.value)} 
                    placeholder="Enter # Episodes"
                  />
                </div>
              <div>
                <div>Genre</div>
                <select value={filterSelections.genre} onChange={(e) => handleFilterChange('genre', e.target.value)}>
                  <option value=""></option>
                  <option value="Action">Action</option>
                  <option value="Adventure">Adventure</option>
                  <option value="Comedy">Comedy</option>
                  <option value="Drama">Drama</option>
                  <option value="Fantasy">Fantasy</option>
                </select>
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="content">
  {jsonData.map((data, index) => (
    <div key={index} className="container">
      {imagesLoaded && <img src={data.image_anime_url} alt={`Anime ${index + 1}`} style={{ maxWidth: '100%', height: 'auto' }} />}      
      <p>{data.english_title}</p>
      <p>{data.genre}</p>
      <p>{data.score}</p>
      <p className="synopsis">{data.synopsis}</p> {/* Use class name for targeting */}
    </div>
  ))}
  </div>
</div>
);}

export default App;
