import React, { useState } from 'react';

const SearchMovie: React.FC = () => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    alert(`Searching for: ${query}`);
  };

  return (
    <div>
      <h3>Search Movie</h3>
      <input
        type="text"
        placeholder="Enter movie title"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch} style={buttonStyle}>Search</button>
    </div>
  );
};

const buttonStyle: React.CSSProperties = {
  backgroundColor: '#007bff',
  color: 'white',
  border: 'none',
  padding: '10px 15px',
  borderRadius: '5px',
  cursor: 'pointer',
};

export default SearchMovie;
