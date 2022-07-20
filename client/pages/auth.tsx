import { useState } from 'react'
import type { NextPage } from 'next'
import Head from 'next/head'
import { useRouter } from "next/router"
import Link from 'next/link'
import base_url from "../base_url";
// import isEmail from 'validator/lib/isEmail';



const Auth: NextPage = () => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    // const [token, setToken] = useState();
    console.log(email)
    console.log(password)

    const router = useRouter()

    function setToken(userToken: any) {
        sessionStorage.setItem('token', JSON.stringify(userToken));
    }

    function getToken() {
        const tokenString = sessionStorage.getItem('token');
        const userToken = JSON.parse(tokenString || '');
        return userToken
    }

    const handleLogin = () => {
        fetch(base_url + '/auth/token', {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('username:password'),
                'Content-Type': 'application/x-www-form-urlencoded'
                // 'Content-Type': 'application/json',
            },
            body:
                `username=${email}&password=${password}`
        })
            .then(response => response.json())
            .then(data => {
                setToken(data.access_token)
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }


    const handleMe = () => {
        const token = getToken()
        console.log(token)
        fetch(base_url + `/auth/me`, {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    const handleDelete = () => {
        const token = getToken()
        console.log(token)
        fetch(base_url + `/user/user`, {
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    const handleSubmit = () => {
        fetch(base_url + '/user/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "username": email,
                "hashed_password": password,
                "name": email,
                "surname": "hui5",
                "age": Math.floor(Math.random() * 100)
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    return (
        <div>
            <Head>
                <title>Auth page!</title>
                <meta name="auth" content="initial-scale=1.0, width=device-width" />
                <link rel="icon" href="/hackathon lohgo.png" />
            </Head>
            <div className="relative flex flex-col justify-center min-h-screen overflow-hidden">
                <div className="w-full p-6 m-auto bg-white border-t-4 border-purple-600 rounded-md shadow-md border-top lg:max-w-md">
                    <h1 className="text-3xl font-semibold text-center text-purple-700">LOS POLLOS</h1>
                    <form className="mt-6">
                        <div>
                            <label htmlFor="email" className="block text-sm text-gray-800">Username</label>
                            <input type="text" placeholder="email" onChange={(e) => setEmail(e.target.value)} className="block w-full px-4 py-2 mt-2 text-purple-700 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40" />
                        </div>
                        <div className='mt-4'>
                            <div>
                                <label htmlFor="password" className="block text-sm text-gray-800">Password</label>
                                <input type="password" placeholder="password" onChange={e => setPassword(e.target.value)} className="block w-full px-4 py-2 mt-2 text-purple-700 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40" />
                                <a href="#" className="text-xs text-gray-600 hover:underline">Forget Password?</a>
                                {/* Change the <a> tag to the link */}
                                <div>
                                    <Link href='/'>
                                        <button type="submit" onClick={handleLogin} className="block w-full px-4 py-2 mt-4 text-white bg-purple-600 border border-purple-600 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-purple-300 focus:ring focus:ring-opacity-40">
                                            Log In
                                        </button>
                                    </Link>
                                    <Link href='/'>
                                        <button type="submit" onClick={handleDelete} className="block w-full px-4 py-2 mt-4 text-white bg-purple-600 border border-purple-600 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-purple-300 focus:ring focus:ring-opacity-40">
                                            DELETE ME
                                        </button>
                                    </Link>
                                    {/* <Link href='/'>
                                        <button type="submit" onClick={handleSubmit} className="block w-full px-4 py-2 mt-4 text-white bg-purple-600 border border-purple-600 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-purple-300 focus:ring focus:ring-opacity-40">
                                            CREATE USER
                                        </button>
                                    </Link> */}
                                </div>
                            </div>
                        </div>
                    </form>
                    <p className="mt-8 text-xs font-light text-center text-gray-700"> Dont have an account?
                        <Link href="/signUp">
                            <a>
                                <button className="font-medium text-purple-600 hover:underline"> Sign up</button>
                            </a>
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    )
}

export default Auth
