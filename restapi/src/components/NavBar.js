import React from 'react'
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
const NavBar = () => {
  return (
    <div>
      <Navbar bg="dark" data-bs-theme="light">
        <Container>
          <Navbar.Brand >Recipes</Navbar.Brand>
          <Nav className="me-auto">
            <Nav.Link className='nav-link active text-white' >Home</Nav.Link>
            <Nav.Link className='nav-link active text-white' >Sign Up</Nav.Link>
            <Nav.Link className='nav-link active text-white'>Login</Nav.Link>
            <Nav.Link className='nav-link active text-white' >Create Recipe</Nav.Link>
            <Nav.Link className='nav-link active text-white' >Log Out</Nav.Link>
          </Nav>
        </Container>
      </Navbar>
    </div>
  )
}

export default NavBar