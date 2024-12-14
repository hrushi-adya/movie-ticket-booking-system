import { useNavigate } from "react-router-dom";

interface TrabsactionCardProps {
    transaction_id: string;
    transaction_movie_id: string;
    transaction_amount: string;
    transaction_date: string
}

const MovieCard: React.FC<TrabsactionCardProps> = ({ transaction_id, transaction_movie_id, transaction_amount, transaction_date }) => {

    const navigate = useNavigate();
    const handleBook = () => {
        navigate('/book', {
            state: {
                transaction_id,
                transaction_movie_id,
                transaction_amount,
                transaction_date
            }
        });
    };
    const handleSelect = () => {
        navigate('/select', {
            state: {
                transaction_id,
                transaction_movie_id,
                transaction_amount,
                transaction_date
            }
        });
    }


    return (
        <div style={cardStyle}>
            <div style={cardContentStyle}>
                <h3>{transaction_id}</h3>
                <p>Movie: {transaction_movie_id}</p>
                <p>Amount: {transaction_amount}</p>
                <p>Date: {transaction_date}</p>
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

export default MovieCard;