import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import MovieCard from './MovieCard';
import MyShowsCard from './MyShowCard';

const MyShows: React.FC = () => {
    const { isLoggedIn, username } = useAuth();
    const location = useLocation();
    const [responseMessage, setResponseMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const navigate = useNavigate();
    // const state = location.state as { isLoggedIn?: boolean; username?: string };
    // use the user name and pass it along with the request to the API to get movies for a specifc user 
    const apiGatewayUrl = 'https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-GetWatchList-DEV';
    const [movies, setMovies] = useState<any[]>([]);

    console.log("Username: ", username);
    const fetchData = async () => {
        try {
            const response = await fetch(`${apiGatewayUrl}?user_id=${username}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            console.log('Data:', data);
            if (response.ok) {
                console.log('Data:', data);
                setMovies(data); // Update state with fetched movies
            } else {
                setErrorMessage(data.message || 'Failed to get WatchList from API.');
            }
            console.log("MOVIEE")
            // movies.map((movie: any) => {
            //     console.log("MOVIEEEE")
            //     console.log(`Name: ${movie.movie_name}`);
            //     console.log(`Description: ${movie.movie_description}`);
            //     console.log(`Rating: ${movie.ticket_price}`);
            //     console.log("EEEEIEVOM")
            // });
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
                            <MyShowsCard
                                key={index}
                                title={movie.movie_name}
                                show_date={movie.show_date}
                                ticket_quantity={movie.ticket_quantity}                              
                                transaction_id={movie.transaction_id}
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

export default MyShows;
