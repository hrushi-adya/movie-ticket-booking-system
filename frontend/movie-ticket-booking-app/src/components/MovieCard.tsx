import React from 'react';
import { useNavigate } from 'react-router-dom';

interface MovieCardProps {
    title: string;
    description: string;
    image: string;
    rating: string;
}

const MovieCard: React.FC<MovieCardProps> = ({ title, description, image, rating }) => {

    const navigate = useNavigate();
    const handleBook = () => {
        navigate('/book', { state: { title, description } });
    };
    const handleSelect = () => {
        navigate('/select', { state: { title, description } });
    } 


    return (
        <div style={cardStyle}>
            <img src={image} alt={title} style={imageStyle} />
            <div style={cardContentStyle}>
                <h3>{title}</h3>
                <p>{description}</p>
                <p><strong>Rating:</strong> {rating}</p>
                <button style={buttonStyle} onClick={handleBook}>Book</button>
                <button style={buttonStyle} onClick={handleSelect}>Select</button>
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
