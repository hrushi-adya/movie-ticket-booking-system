import { useNavigate } from "react-router-dom";

interface MovieCardProps {
    title: string;
    total_sales: string;
    total_cost: string;
}

const SalesCard: React.FC<MovieCardProps> = ({ title, total_sales, total_cost}) => {

    const navigate = useNavigate();
    const handleBook = () => {
        navigate('/book', { 
            state: { 
                title, 
                total_sales, 
                total_cost 
            } 
        });
    };
    const handleSelect = () => {
        navigate('/select', { 
            state: { 
                title, 
                total_sales, 
                total_cost
            } 
        });
    } 


    return (
        <div style={cardStyle}>
            <div style={cardContentStyle}>
                <h3>{title}</h3>
                <p>{total_sales} Revenue: {total_cost}</p>
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

export default SalesCard;