import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext';
interface BookTicketProps {
    movie: {
        title: string;
        description: string;
    };
}

const BookTicket: React.FC<BookTicketProps> = ({ movie }) => {

    const location = useLocation();
    const { username } = useAuth();
    const { title, description } = location.state as { title: string; description: string };

    const [name, setName] = useState(username ||'');
    const [theatre, setTheatre] = useState('');
    const [seats, setSeats] = useState(1);
    const navigate = useNavigate();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        alert(`Ticket booked successfully for ${movie.title}!`);
        navigate('/'); // Redirect back to the home page
    };

    return (
        <div style={formContainerStyle}>
            <h2>Book Ticket for {movie.title}</h2>
            <form onSubmit={handleSubmit} style={formStyle}>
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <label>Theatre:</label>
                            </td>
                            <td>
                                <select value={theatre} onChange={(e) => setTheatre(e.target.value)} required>
                                    <option value="">Select Theatre</option>
                                    <option value="Theatre 1">Theatre 1</option>
                                    <option value="Theatre 2">Theatre 2</option>
                                    <option value="Theatre 3">Theatre 3</option>
                                </select>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Your Name:</label>
                            </td>
                            <td>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    required
                                />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Number of Seats:</label>
                            </td>
                            <td>
                                <input
                                    type="number"
                                    value={seats}
                                    onChange={(e) => setSeats(Number(e.target.value))}
                                    min="1"
                                    required
                                />
                            </td>
                        </tr>
                    <tr>
                        <td>
                            <label>Movie Name:</label>
                        </td>
                        <td>
                            <input type="text" value={movie.title} readOnly />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Show Time:</label>
                        </td>
                        <td>
                            <input type="text" required />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Ticket Price:</label>
                        </td>
                        <td>
                            <input type="number" min="0" step="0.01" required />
                        </td>
                    </tr>
                    </tbody>
                </table>
                <button type="submit" style={buttonStyle}>Confirm Booking</button>
            </form>
        </div>
    );
};

const formContainerStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginTop: '50px',
};

const formStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    width: '300px',
    gap: '15px',
};

const buttonStyle: React.CSSProperties = {
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    padding: '10px',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '16px',
};

export default BookTicket;
