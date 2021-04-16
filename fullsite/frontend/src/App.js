import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Button from 'react-bootstrap/Button';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
import ElementsForm from './components/Form/ElementsForm'
import ConnForm from './components/Form/ConnForm'
import ProdForm from './components/Form/ProdForm'
import LoginModal from './components/Base/LoginModal'
import ConnListContainer from './containers/ConnListContainer'
import ElementListContainer from './containers/ElementListContainer'
import ProdListContainer from './containers/ProdListContainer'


import React, { useState} from 'react';
import {BrowserRouter, Route, Link, Switch} from 'react-router-dom';

function App() {
  const [modalState, setModalState] = useState(false);
     const onButtonClick=(state) => {setModalState(state)}


     // POZMIENIAĆ WYGLĄD MENU I SPRAWIC BY TORZENIE NOWYCH PRZECHODZILO PRZEZ KONTENERY
  return (
    <BrowserRouter>
        <Navbar bg="primary" variant="dark" expand="lg">
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link as={Link} to="/">Home</Nav.Link>
              <NavDropdown title="Zarządzenie RB" id="basic-nav-dropdown1">
                <NavDropdown.Item ><Link to="/element/new">Nowy użytkownik RB</Link></NavDropdown.Item>
                <NavDropdown.Item ><Link to="/connections/new">Nowe połączenie</Link></NavDropdown.Item>
                <NavDropdown.Item ><Link to="/producers/new">Nowy wytwórca</Link></NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item ><Link to="/element/POB">Lista POB</Link></NavDropdown.Item>
                <NavDropdown.Item ><Link to="/element/SE">Lista SE</Link></NavDropdown.Item>
                <NavDropdown.Item ><Link to="/connections">Lista połączeń</Link></NavDropdown.Item>                
                <NavDropdown.Item ><Link to="/producers">Lista wytwórców</Link></NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>

        {/* if statement for changing betweenh log in and log out button */}

        <Button variant={'secondary'} onClick={() => onButtonClick(true)}>Zaloguj</Button>

        <Route path="/RB"><ConnForm/></Route>
        </Navbar>
  
      <Breadcrumb>
        <Breadcrumb.Item href="#">Home</Breadcrumb.Item>
        <Breadcrumb.Item href="https://getbootstrap.com/docs/4.0/components/breadcrumb/">
          Library
        </Breadcrumb.Item>
        <Breadcrumb.Item active>Data</Breadcrumb.Item>
      </Breadcrumb>

      
      <LoginModal modalState={{modalState: modalState, setModalState:setModalState}}/>
      <div className="container mt-2" style={{ marginTop: 40 }}>

    <Switch>
      <Route exact={true} path="/"></Route>  
      <Route path="/connections/new"><ConnForm/></Route>
      <Route path="/producers/new"><ProdForm /></Route>
      <Route path="/element/new"><ElementsForm /></Route>
      <Route path="/connections" component={ConnListContainer} />
      <Route path="/element/POB" component={ElementListContainer} />
      <Route path="/element/SE" component={ElementListContainer} />
      <Route path="/producers" component={ProdListContainer} />
    </Switch>  
      
      
      </div>
      

 
    </BrowserRouter>
  );
}

export default App;
