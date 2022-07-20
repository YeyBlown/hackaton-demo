import { useState, useEffect } from 'react'
import Link from 'next/link'
import React from 'react'



const Header = () => {
  const [query, setQuery] = useState('')
  console.log(query)

  useEffect(() => {
    // Perform localStorage action
    const item = localStorage.getItem('token')
  }, [])
  // const token = sessionStorage.getItem('token')

  const handleLogout = () => {
    return sessionStorage.removeItem('token')
  }
  // const search = () => {
  //   fetch(`http://games-server:8000/user/search`, {
  //           method: 'GET',
  //           headers: {
  //               'Content-Type': 'application/json',
  //           },
  //           body: JSON.stringify({query: query})
  //       })
  //           .then(response => response.json())
  //           .then(data => {
  //               console.log('Success:', data);
  //           })
  //           .catch((error) => {
  //               console.error('Error:', error);
  //           });
  // }


  return (
    <div className="navbar bg-base-100 rounded-lg mb-3 bg-primary ">
      <div className="flex-1">
        <Link href="/">
          <a className="btn btn-ghost normal-case text-xl">Los Pollos Hermanos</a>
        </Link>
      </div>
      <div className="flex-none gap-2">
        <div className="form-control">
          <input
            type="text"
            placeholder="Search..."
          // onChange={event => { this.setQuery({ query: event.target.value }) }}
          // onKeyPress={event => {
          //   if (event.key === 'Enter') {
          //     this.search()
          //   }
          // }
          // }
          />
        </div>
        <Link href='/auth'>
          <a>
            <button className="btn btn-ghost"> Authorize </button>
          </a>
        </Link>
        <Link href='/'>
          <a>
            <button className="btn btn-ghost" onClick={handleLogout}> Logout</button>
          </a>
        </Link>
        <div className="dropdown dropdown-end" >
          <label className="btn btn-ghost btn-circle avatar">
            <div className="w-10 rounded-full">
              <img src="https://placeimg.com/80/80/people" />
            </div>
          </label>
          <ul className="mt-3 p-2 shadow menu menu-compact dropdown-content bg-base-100 rounded-box w-52">
            <li>
              <a className="justify-between">
                Profile
                {/* <span className="badge">New</span> */}
              </a>
            </li>
            <li><a>Settings</a></li>
            <li><a>Logout</a></li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Header