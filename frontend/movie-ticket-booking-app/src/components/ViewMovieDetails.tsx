import React from 'react';
import { useParams } from 'react-router-dom';

interface MovieDetailsProps {
    id: string;
    title: string;
    description: string;
    releaseDate: string;
    rating: number;
    genre: string;
}

const ViewMovieDetails: React.FC = () => {
    const { movieId } = useParams<{ movieId: string }>();
    const [movieDetails, setMovieDetails] = React.useState<MovieDetailsProps | null>(null);

    
    React.useEffect(() => {
        // Fetch movie details from an API or a static source
        const fetchMovieDetails = async () => {
            // Replace with your API call
            const response = await fetch(`/api/movies/${movieId}`);
            const data = await response.json();
            setMovieDetails(data);
        };

        fetchMovieDetails();
    }, [movieId]);

    if (!movieDetails) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>{movieDetails.title}</h1>
            <p>{movieDetails.description}</p>
            <p>Release Date: {movieDetails.releaseDate}</p>
            <p>Rating: {movieDetails.rating}</p>
            <p>Genre: {movieDetails.genre}</p>
        </div>
    );
};

export default ViewMovieDetails;