import { useNavigate } from "react-router-dom";

interface SearchResultCardProps {
    movie_name: string;
    genre: string;
    movie_description: string;
    movie_director: string
    movie_showtime: string;
    release_date: string;
    ticket_price: string;
}

const SearchResultCard: React.FC<SearchResultCardProps> = ({ movie_name, genre, movie_description, movie_director, movie_showtime, release_date, ticket_price }) => {

    const navigate = useNavigate();
    const handleBook = () => {
        navigate('/book', {
            state: {
                movie_name,
                genre,
                movie_description,
                movie_director,
                movie_showtime,
                release_date,
                ticket_price
            }
        });
    };
    const handleSelect = () => {
        navigate('/select', {
            state: {
                movie_name,
                genre,
                movie_description,
                movie_director,
                movie_showtime,
                release_date,
                ticket_price
            }
        });
    }

    return (
        <div style={cardStyle}>
            <div style={cardContentStyle}>
                <h3>{movie_name}</h3>
                <p>Genre: {genre}</p>
                <p>Description: {movie_description}</p>
                <p>Director: {movie_director}</p>
                <p>Showtime: {movie_showtime}</p>
                <p>Release Date: {release_date}</p>
                <p>Ticket Price: {ticket_price}</p>
            </div>
        </div>
    );
};

const cardStyle: React.CSSProperties = {
    border: '1px solid #ccc',
    borderRadius: '8px',
    overflow: 'hidden',
    width: '300px',
    margin: '20px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
};

const imageStyle: React.CSSProperties = {
    width: '100%',
    height: '200px',
    objectFit: 'cover',
};

const cardContentStyle: React.CSSProperties = {
    padding: '15px',
};

const buttonStyle: React.CSSProperties = {
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '16px',
};

export default SearchResultCard;