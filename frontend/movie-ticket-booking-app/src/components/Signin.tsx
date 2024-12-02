import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

// import '../styles/Form.css';

const Login: React.FC = () => {
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [responseMessage, setResponseMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    const navigate = useNavigate();
    const { login } = useAuth();


    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });

    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        console.log('Login Data:', formData);
        console.log(formData.username);
        console.log(formData.password)

        const payload = {
            user_id: formData.username,
            password: formData.password,
        };
        console.log(payload);

        const apiGatewayUrl = 'https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-SignIn-DEV';

        try {
            const response = await fetch(apiGatewayUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            const result = await response.json();
            console.log(result);
            const profileType = result ? result.data.profile_type : null;
            console.log("profile type: ", profileType);
            if (response.ok) {
                if (profileType === 'admin') {
                    login(formData.username, 'admin'); // Update authentication state
                    navigate('/'); // Redirect to the home page
                } else if (profileType === 'user') {
                    login(formData.username, 'user');
                    navigate('/');
                }
                setResponseMessage('Sign In successful!');
            } else {
                setErrorMessage(result.message || 'Sign In failed. Please try again.');
            }
        } catch (error) {
            setErrorMessage('Network error. Please try again.');
        } finally {
            setIsLoading(false);
        }

        // if (formData.username === 'admin' && formData.password === 'password') {
        //     alert('Login successful!');
        //     login(formData.username, 'admin'); // Update authentication state
        //     navigate('/'); // Redirect to the home page
        // } else if (formData.username === 'user' && formData.password === 'password') {
        //     alert('Login successful!');
        //     login(formData.username, 'user'); // Update authentication state
        //     navigate('/'); // Redirect to the home page
        // } else {
        //     alert('Invalid credentials. Please try again.');
        // }
    };

    //   setTimeout(() => {
    //     navigate('/', { state: { isLoggedIn: true, username: formData.username } });
    //   }, 500);

    return (
        <div className="form-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>-
            <div style={{ border: '2px solid black', padding: '20px', borderRadius: '3px', textAlign: 'center' }}>
                <h2>Login</h2>
                <hr style={{ border: '1px solid black', width: '100%' }} />
                <form onSubmit={handleSubmit}>
                    <table style={{ margin: '0 auto' }}>
                        <tbody>
                            <tr>
                                <td><label>Username:</label></td>
                                <td><input type="text" name="username" value={formData.username} onChange={handleChange} required /></td>
                            </tr>
                            <tr>
                                <td><label>Password:</label></td>
                                <td><input type="password" name="password" value={formData.password} onChange={handleChange} required /></td>
                            </tr>
                            <tr>
                                <td colSpan={2} style={{ textAlign: 'center' }}>
                                    <button type="submit">Login</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </form>
            </div>
        </div>
    );
};

export default Login;
function setErrorMessage(arg0: any) {
    throw new Error('Function not implemented.');
}

