import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Button from 'react-bootstrap/Button';
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
  const [loginState, setLoginState] = useState(false);
  const onButtonClick=(state) => {
    setModalState(state)}



  const LogOut = () => {
    localStorage.clear()
    setLoginState(false)

  }

  


  return (
    <BrowserRouter>
        <Navbar bg="primary" variant="dark" expand="lg">
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link as={Link} to="/">Home</Nav.Link>
              <NavDropdown title="Zarządzenie RB" id="basic-nav-dropdown1">
                <NavDropdown.Item as={Link} to="/element/new">Nowy użytkownik RB</NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/connections/new">Nowe połączenie</NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/producers/new">Nowy wytwórca</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item as={Link} to="/element/POB">Lista POB</NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/element/SE">Lista SE</NavDropdown.Item>
                <NavDropdown.Item as={Link} to="/connections">Lista połączeń</NavDropdown.Item>                
                <NavDropdown.Item as={Link} to="/producers">Lista wytwórców</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>


        {(localStorage.getItem('token')) ?
        <div>
        <Button variant={'secondary'}>{localStorage.getItem('username')}</Button>     
        <Button variant={'secondary'} onClick={() => LogOut()}>Wyloguj</Button>
        </div>
        :
        <div>
        Niezalogowano
        <Button variant={'secondary'} onClick={() => onButtonClick(true)}>Zaloguj</Button>
        </div>
        }


      </Navbar>
      <LoginModal modalState={{modalState: modalState, setModalState:setModalState}}
       username={setLoginState}/>
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
