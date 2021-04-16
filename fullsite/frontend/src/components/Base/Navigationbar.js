import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Button from 'react-bootstrap/Button';
import { Link, Route } from 'react-router-dom';
import ConnFrom from '../Forms/ConnForm'


function Navigationbar({setModalState})  {

const onButtonClick=(state) => {setModalState(state)}

return (

<Navbar bg="primary" variant="dark" expand="lg">
  <Navbar.Toggle aria-controls="basic-navbar-nav" />
  <Navbar.Collapse id="basic-navbar-nav">
    <Nav className="mr-auto">
      <Nav.Link>Home</Nav.Link>
      <NavDropdown title="Zarządzenie RB" id="basic-nav-dropdown">
        <NavDropdown.Item ><Link to='/RB'>Nowy użytkownik RB</Link></NavDropdown.Item>
        <NavDropdown.Item >Nowe połączenie</NavDropdown.Item>
        <NavDropdown.Item >Nowy wytwórca</NavDropdown.Item>
      </NavDropdown>
    </Nav>
  </Navbar.Collapse>

{/* if statement for changing betweenh log in and log out button */}

<Button variant={'secondary'} onClick={() => onButtonClick(true)}>Zaloguj</Button>

<Route path="/RB"><ConnFrom/></Route>
</Navbar>


)

}

export default Navigationbar


