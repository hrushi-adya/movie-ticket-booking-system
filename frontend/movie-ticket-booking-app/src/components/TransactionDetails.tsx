import React, { ReactEventHandler, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import TransactionCard from './TransactionCard';

const TransactionDetails: React.FC = () => {

    const { isLoggedIn, username } = useAuth();
    const location = useLocation();
    const [responseMessage, setResponseMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [startDate, setStartDate] = useState<string>('');
    const [endDate, setEndDate] = useState<string>('');
    const navigate = useNavigate();
    // const state = location.state as { isLoggedIn?: boolean; username?: string };
    // use the user name and pass it along with the request to the API to get movies for a specifc user 
    const apiGatewayUrl = 'https://858a5if44a.execute-api.us-east-2.amazonaws.com/dev/MTB-API-TransactionDetails-DEV';
    const [transactions, setTransaction] = useState<any[]>([]);

    console.log("Username: ", username);
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const formatToDashDate = (date: string) => {
            const [year, month, day] = date.split("-");
            return `${month}-${day}-${year}`;
        };

        const formattedStartDate = formatToDashDate(startDate);
        const formattedEndDate = formatToDashDate(endDate);

        console.log("Formatted Start Date: ", formattedStartDate);
        console.log("Formatted End Date: ", formattedEndDate);

        console.log("Start Date: ", startDate);
        console.log("End Date: ", endDate);
        console.log("Testing");
        try {
            const response = await fetch(`${apiGatewayUrl}?start_date=${formattedStartDate}&end_date=${formattedEndDate}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const data = await response.json();
            console.log('Data:', data);
            if (response.ok) {
                console.log('Data:', data);
                setTransaction(data); // Update state with fetched movies
            } else {
                setErrorMessage(data.message || 'Failed to get WatchList from API.');
            }
        } catch (error) {
            setErrorMessage('Error calling API. Please try again later.');
        } finally {
            setIsLoading(false);
        }
    };

    // fetchData();

    return (
        <div>
            <div>
                <div style={containerStyle}>
                    <form onSubmit={handleSubmit} style={formStyle}>
                        <label>
                            Start Date:
                            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} required />
                        </label>
                        <label>
                            End Date:
                            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} required />
                        </label>
                        <button type="submit">Submit</button>
                    </form>
                </div>
                <div style={gridStyle}>
                    {transactions.map((transaction, index) => (
                        <TransactionCard
                            key={index}
                            transaction_id={transaction.transaction_id}
                            transaction_movie_id={transaction.transaction_movie_id}
                            transaction_amount={transaction.transaction_amount}
                            transaction_date={transaction.transaction_date}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

const gridStyle: React.CSSProperties = {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    marginTop: '20px',
};

const containerStyle: React.CSSProperties = {
    padding: '50px',
    maxWidth: '900px',
    margin: '0 auto',
};

const formStyle: React.CSSProperties = {
    display: 'flex',
    flexDirection: 'column',
    width: '300px',
    gap: '15px',
};

export default TransactionDetails;
