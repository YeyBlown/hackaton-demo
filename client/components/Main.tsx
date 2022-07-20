import React, { useState, useEffect } from "react";
import base_url from '../base_url.js';


export default function App() {

    const [data, setData] = useState<any[]>([]);
    //Fetches data on a load
    useEffect(() => {
        fetch(base_url + "/user/view_all")
            .then((response) => response.json())
            .then((data) => setData(data))
            .catch((error) => console.log("Error ", error));
    }, []);


    // const handleDelete = () => {
    //     fetch('http://localhost:8000/user/create', {
    //         method: 'DELETE',   
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify({
                
    //         }),
    //     })
    //         .then(response => response.json())
    //         .then(data => {
    //             console.log('Success:', data);
    //         })
    //         .catch((error) => {
    //             console.error('Error:', error);
    //         });
    // }


    return (
        <div className="wrapper">
            {data.map((user, index) => (
                <div key={index} className="card">
                    {/* <img src={user.picture.large} alt="" /> */}
                    <div className="name">
                        <p>
                            Username: {user.name}
                        </p>
                        <p>
                            Description: {user.description}
                        </p>
                        <p>
                            Age: {user.age}
                        </p>
                        
                    </div>
                </div>
            ))}
        </div>
    );
}
// {`Username:${user.name} Description${user.description} Age:${user.age}`}