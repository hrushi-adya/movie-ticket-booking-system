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
    // use the user name and pass it along with the request to the API to get movies for a specifc user 
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
                setMovies(data.movies); // Update state with fetched movies
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

    const movies1 = [
        {
            title: 'Inception',
            description: 'A thief with the ability to enter dreams takes on a heist in a dream world.',
            image: 'https://via.placeholder.com/300x200?text=Inception',
            rating: '8.8',
        },
        {
            title: 'Interstellar',
            description: 'A group of explorers travel through a wormhole in space.',
            image: 'https://via.placeholder.com/300x200?text=Interstellar',
            rating: '8.6',
        },
        {
            title: 'The Dark Knight',
            description: 'Batman faces the Joker in Gotham City.',
            image: 'https://via.placeholder.com/300x200?text=The+Dark+Knight',
            rating: '9.0',
        },
        {
            title: 'Avatar',
            description: 'A paraplegic marine explores a lush alien world.',
            image: 'https://via.placeholder.com/300x200?text=Avatar',
            rating: '7.9',
        },
        {
            title: 'Inception',
            description: 'A thief with the ability to enter dreams takes on a heist in a dream world.',
            image: 'https://via.placeholder.com/300x200?text=Inception',
            rating: '8.8',
        },
        {
            title: 'Interstellar',
            description: 'A group of explorers travel through a wormhole in space.',
            image: 'https://via.placeholder.com/300x200?text=Interstellar',
            rating: '8.6',
        },
        {
            title: 'The Dark Knight',
            description: 'Batman faces the Joker in Gotham City.',
            image: 'https://via.placeholder.com/300x200?text=The+Dark+Knight',
            rating: '9.0',
        },
        {
            title: 'Avatar',
            description: 'A paraplegic marine explores a lush alien world.',
            image: 'https://via.placeholder.com/300x200?text=Avatar',
            rating: '7.9',
        }
    ];

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
                    {/* <h1>Welcome Back, {username}!</h1>
                    <p>Thank you for logging in. Explore your dashboard below.</p> */}
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
