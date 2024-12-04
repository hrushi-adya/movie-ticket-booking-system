import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import SalesCard from './SalesCard';

const SalesDashboard: React.FC = () => {
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

    console.log("Username: ", username);
    const fetchData = async () => {
        try {
            const response = await fetch(apiGatewayUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            console.log('Data:', data);
            if (response.ok) {
                console.log('Data inside res ok:', data);
                setMovies(data.movies); // Update state with fetched movies
                console.log('Movies:', movies);
            } else {
                setErrorMessage(data.message || 'Failed to get WatchList from API.');
            }
            console.log("MOVIEE")
            // data.map((movies: any) => {
            //     console.log("MOVIEEEE")
            //     console.log(`Name: ${movies.movie_name}`);
            //     console.log(`Description: ${movies.movie_description}`);
            //     console.log(`Rating: ${movies.ticket_price}`);
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
                            <SalesCard
                                key={index}
                                title={movie.movie_name}
                                total_sales={movie.total_sales}
                                total_cost={movie.total_tickets_business}
                            />
                        ))}
                    </div>
                </div>
            ) : (
                <div>
                    <p>No Movie present</p>

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

export default SalesDashboard;
