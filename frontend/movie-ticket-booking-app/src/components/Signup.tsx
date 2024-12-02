import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
// import '../styles/Form.css';

const SignUp: React.FC = () => {
    const [formData, setFormData] = useState({ email: '', password: '', firstname: '', lastname: '', phone: '', profile_type: '' });
    const [responseMessage, setResponseMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const navigate = useNavigate(); // Hook for navigation

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log('Sign Up Data:', {
            email: formData.email,
            password: formData.password,
            user_id: formData.email,
            firstname: formData.firstname,
            lastname: formData.lastname,
            phone: formData.phone,
            profile_type: formData.profile_type
        });

        console.log(formData);

        const payload = {
            email: formData.email,
            password: formData.password,
            first_name: formData.firstname,
            last_name: formData.lastname,
            phone: formData.phone,
            profile_type: formData.profile_type,
            user_id: formData.email,
        };

        console.log(payload);
        const apiGatewayUrl = 'https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-SignUp-DEV';

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
                navigate('/signin');
                setResponseMessage('Signup successful!');
            } else {
                setErrorMessage(result.message || 'Signup failed. Please try again.');
            }
        } catch (error) {
            setErrorMessage('Network error. Please try again.');
        } finally {
            setIsLoading(false);
        }

        // setTimeout(() => { navigate('/signin'); }, 500);
    };

    return (
        <div className="form-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>-
            <div style={{ border: '2px solid black', padding: '20px', borderRadius: '3px', textAlign: 'center' }}>
                <h2>Sign Up</h2>
                <hr style={{ border: '1px solid black', width: '100%' }} />

                <form onSubmit={handleSubmit}>
                    <table>
                        <tr>
                            <td>
                                <label>Email ID:</label>
                            </td>
                            <td>
                                <input type="email" name="email" value={formData.email} onChange={handleChange} required />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Password:</label>
                            </td>
                            <td>
                                <input type="password" name="password" value={formData.password} onChange={handleChange} required />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>First Name:</label>
                            </td>
                            <td>
                                <input type="text" name="firstname" value={formData.firstname} onChange={handleChange} required />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Last Name:</label>
                            </td>
                            <td>
                                <input type="text" name="lastname" value={formData.lastname} onChange={handleChange} required />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Phone:</label>
                            </td>
                            <td>
                                <input type="text" name="phone" value={formData.phone} onChange={handleChange} required />
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label>Profile Type:</label>
                            </td>
                            <td>
                                <input type="radio" name="profile_type" value="admin" onChange={handleChange}
                                    checked={formData.profile_type === "admin"} required /> Admin
                                <input type="radio" name="profile_type" value="user" onChange={handleChange}
                                    checked={formData.profile_type === "user"} required /> User
                            </td>
                        </tr>
                    </table>
                    <button type="submit">Sign Up</button>
                </form>
            </div>
        </div>
    );
};

export default SignUp;
