import React from 'react';
import { useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext';
import MovieCard from './MovieCard';

const Home: React.FC = () => {
    const { isLoggedIn, username } = useAuth();
    const location = useLocation();
    // const state = location.state as { isLoggedIn?: boolean; username?: string };
    const movies = [
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
                                title={movie.title}
                                description={movie.description}
                                image={movie.image}
                                rating={movie.rating}
                            />
                        ))}
                    </div>
                    <h1>Welcome Back, {username}!</h1>
                    <p>Thank you for logging in. Explore your dashboard below.</p>
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
