import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SearchResultCard from './SearchResultCard';

const SearchMovie: React.FC = () => {
  const [query, setQuery] = useState('');
  const [responseMessage, setResponseMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const navigate = useNavigate();
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Movie Name:', query);
    const apiGatewayUrl = 'https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-Movie-DEV';

    try {
      const response = await fetch(`${apiGatewayUrl}?movie_name=${query}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const result = await response.json();
      if (response.ok) {
        console.log('Search movie results:', result);
        const movies = Array.isArray(result.movies) ? result.movies : [result.movies];
        setSearchResults(movies)
        setResponseMessage('Movie searched successfully!');
      } else {
        setErrorMessage(result.message || 'Search Operation failed. Please try again.');
      }
    } catch (error) {
      setErrorMessage('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} style={formStyle}>
        <h3>Search Movie</h3>
        <input
          type="movie name"
          placeholder="Enter movie title"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" style={buttonStyle}>Search</button>
      </form>
      <div style={gridStyle}>
        {searchResults.map((result, index) => (
          <SearchResultCard
            key={index}
            movie_name={result.movie_name}
            genre={result.genre}
            movie_description={result.movie_description}
            movie_director={result.movie_director}
            movie_showtime={result.movie_showtime}
            release_date={result.release_date}
            ticket_price={result.ticket_price}
          />
        ))}
      </div>
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

const gridStyle: React.CSSProperties = {
  display: 'flex',
  flexWrap: 'wrap',
  justifyContent: 'center',
  marginTop: '20px',
};

const formStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: '10px',
};

export default SearchMovie;
