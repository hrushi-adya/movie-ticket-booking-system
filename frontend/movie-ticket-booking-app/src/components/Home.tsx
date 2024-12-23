import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import MovieCard from './MovieCard';

const Home: React.FC = () => {
    const { isLoggedIn, username } = useAuth();
    const location = useLocation();
    const [responseMessage, setResponseMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const navigate = useNavigate();
    // const state = location.state as { isLoggedIn?: boolean; username?: string };
    const apiGatewayUrl = 'https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-Movie-DEV';
    const [movies, setMovies] = useState<any[]>([]);
    const fetchData = async () => {
        try {
            const response = await fetch(apiGatewayUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            const movies = data.movies;
            console.log(movies);
            if (response.ok) {
                console.log('Movie Data:', movies);
                // const availableMovies = data.movies.filter((movie: any) => movie.movie_available === "True");
                // setMovies(availableMovies); 

                setMovies(data.movies);
            } else {
                setErrorMessage(movies.message || 'Failed to get Movies from API.');
            }
            console.log("MOVIEE")
            movies.map((movie: any) => {
                console.log("MOVIEEEE")
                console.log(`Name: ${movie.movie_name}`);
                console.log(`Description: ${movie.movie_description}`);
                console.log(`Rating: ${movie.ticket_price}`);
                console.log("EEEEIEVOM")
            });
        } catch (error) {
            setErrorMessage('Error calling API. Please try again later.');
        } finally {
            setIsLoading(false);
        }
    };

    fetchData();

    return (
        <div>
            {isLoggedIn ? (
                <div>
                    <div style={gridStyle}>
                        {movies.map((movie, index) => (
                            <MovieCard
                                key={index}
                                title={movie.movie_name}
                                description={movie.movie_description}
                                image={movie.movie_thumbnail}                              
                                rating={movie.rating}
                            />
                        ))}
                    </div>
                </div>
            ) : (
                <div>
                    <h1>Welcome to the Home Page</h1>
                    <p>Please log in to access more features.</p>
                </div>
            )}
        </div>
    );
};

const gridStyle: React.CSSProperties = {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginTop: '20px',
};

export default Home;
