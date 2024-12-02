import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const Profile: React.FC = () => {
    const { username } = useAuth();

    // Default user details
    const [userDetails, setUserDetails] = useState({
        firstName: 'Hrushikesh',
        lastName: 'Adya',
        email: 'adya.hrushikesh@gmail.com',
        phone: '913-915-3790',
    });

    // Handle input changes
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setUserDetails((prevDetails) => ({
            ...prevDetails,
            [name]: value,
        }));
    };

    // Handle form submission
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        alert('Profile updated successfully!');
        console.log('Updated User Details:', userDetails);
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '20px' }}>
            <h1>My Profile</h1>
            <p>Welcome, {username}!</p>
            <form onSubmit={handleSubmit} style={formStyle}>
                <table>
                    <tbody>
                        <tr style={inputGroupStyle}>
                            <td><label>First Name:</label></td>
                            <td>
                                <input
                                    type="text"
                                    name="firstName"
                                    value={userDetails.firstName}
                                    onChange={handleChange}
                                />
                            </td>
                        </tr>
                        <tr style={inputGroupStyle}>
                            <td><label>Last Name:</label></td>
                            <td>
                                <input
                                    type="text"
                                    name="lastName"
                                    value={userDetails.lastName}
                                    onChange={handleChange}
                                />
                            </td>
                        </tr>
                        <tr style={inputGroupStyle}>
                            <td><label>Email:</label></td>
                            <td>
                                <input
                                    type="email"
                                    name="email"
                                    value={userDetails.email}
                                    onChange={handleChange}
                                />
                            </td>
                        </tr>
                        <tr style={inputGroupStyle}>
                            <td><label>Phone:</label></td>
                            <td>
                                <input
                                    type="text"
                                    name="phone"
                                    value={userDetails.phone}
                                    onChange={handleChange}
                                />
                            </td>
                        </tr>
                        <tr>
                            <td colSpan={2} style={{ textAlign: 'center' }}>
                                <button type="submit" style={buttonStyle}>
                                    Update Profile
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </form>
        </div>
    );
};

const formStyle: React.CSSProperties = {
    display: 'inline-block',
    textAlign: 'left',
    marginTop: '20px',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
};

const inputGroupStyle: React.CSSProperties = {
    marginBottom: '15px',
};

const buttonStyle: React.CSSProperties = {
    display: 'block',
    margin: '0 auto',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
};

export default Profile;
