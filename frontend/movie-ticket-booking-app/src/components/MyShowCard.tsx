import { useNavigate } from "react-router-dom";

interface MovieCardProps {
    title: string;
    show_date: string;
    ticket_quantity: string;
    transaction_id: string
}

const MovieCard: React.FC<MovieCardProps> = ({ title, show_date, ticket_quantity, transaction_id }) => {

    const navigate = useNavigate();
    const handleBook = () => {
        navigate('/book', { 
            state: { 
                title, 
                show_date, 
                ticket_quantity, 
                transaction_id 
            } 
        });
    };
    const handleSelect = () => {
        navigate('/select', { 
            state: { 
                title, 
                show_date, 
                ticket_quantity, 
                transaction_id 
            } 
        });
    } 


    return (
        <div style={cardStyle}>
            <div style={cardContentStyle}>
                <h3>{title}</h3>
                <p>{show_date}</p>
                <p>Ticket Quantity {ticket_quantity}</p>
                <p>Transaction ID {transaction_id}</p>
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