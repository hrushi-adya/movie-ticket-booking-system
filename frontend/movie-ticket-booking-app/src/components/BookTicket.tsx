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
    const [responseMessage, setResponseMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const location = useLocation();
    const { username } = useAuth();
    const { title, description } = location.state as { title: string; description: string };
    const [formData, setFormData] = useState({ theatre: '', name: username || '', seats: '', showTime: '', ticketPrice: '15', movieName: title ||'' });
    const [name, setName] = useState(username ||'');
    const [theatre, setTheatre] = useState('');
    const [seats, setSeats] = useState(1);
    const [movieName, setMovieName] = useState('');
    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log('formData', formData);

        const payload = {
            ticket_price: formData.ticketPrice,
            ticket_quantity: formData.seats,
            ticket_showtime: formData.showTime,
            ticket_movie_id: formData.movieName,
            ticket_theater_id: formData.theatre,
            ticket_user_id: formData.name,
            ticket_status: 'booked',
            ticket_transaction_id: 'dummy-transaction-id',
            ticket_payment_status: 'payment-completed',
        };

        console.log('payload', payload);
        const apiGatewayUrl = "https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-BookTicket-DEV"

        try {
            const response = await fetch(apiGatewayUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            const result = await response.json();

            if (response.ok) {
                console.log('Book Ticket Result:', result);
                alert('Movie Ticket Booking successful!');
                navigate('/');
                setResponseMessage('Booking successful!');
            } else {
                setErrorMessage(result.message || 'Booking failed. Please try again.');
            }
        } catch (error) {
            setErrorMessage('Network error. Please try again.');
        } finally {
            setIsLoading(false);
        }

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
                                <select value={theatre} onChange={(e) => { setTheatre(e.target.value); setFormData({ ...formData, theatre: e.target.value }); }} required>
                                    <option value="">Select Theatre</option>
                                    <option value="Lees Summit">Lees Summit</option>
                                    <option value="Warrensburg">Warrensburg</option>
                                    <option value="Kansas City">Kansas City</option>
                                </select>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Your Name:</label>
                            </td>
                            <td>
                                <input type="text" name="name" value={formData.name} onChange={handleChange} required />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Number of Seats:</label>
                            </td>
                            <td>
                                <input type="text" name="seats" value={formData.seats} onChange={handleChange} required />
                            </td>
                        </tr>
                    <tr>
                        <td>
                            <label>Movie Name:</label>
                        </td>
                        <td>
                                <input type="text" name="movieName" value={formData.movieName} onChange={handleChange} required />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Show Time:</label>
                        </td>
                        <td>
                                <input type="text" name="showTime" value={formData.showTime} onChange={handleChange} required />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Ticket Price:</label>
                        </td>
                        <td>
                                <input type="text" name="ticketPrice" value={formData.ticketPrice} onChange={handleChange} required />
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
