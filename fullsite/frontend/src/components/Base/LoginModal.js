import React, { useState} from 'react';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import Col from 'react-bootstrap/Col'
import axios from 'axios'


function LoginModal(props) {

  const [userName, setUserName] = useState('');
  const [password, setPassword] = useState('');

    const handleSubmit = (event) => {
    event.preventDefault();

    const user = {
      username: userName,
      password: password
    };

    axios.post(`http://localhost:8000/AccApp/login/`, user)
    .then(res => {
      if (res.data.token) {
              localStorage.clear();
              localStorage.setItem('token', res.data.token);
              localStorage.setItem('username', user.username);
              props.username(true)
            } else {
              setUserName('');
              setPassword('');
              localStorage.clear();

            }
          });
      handleClose()  
      };


  const handleClose = () => props.modalState.setModalState(false);

  return (
    <>
      <Modal show={props.modalState.modalState} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Zaloguj się!</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <Form.Group controlId="formLoginUser">
                <Form.Label column sm="3">
                  Nazwa
                </Form.Label>
                <Col>
                  <Form.Control placeholder="Nazwa użytkownika" onChange={e => setUserName(e.target.value)}/>
                </Col>
            </Form.Group>
        <Form.Group controlId="formLoginPassword">
                <Form.Label column sm="3">
                  Hasło
                </Form.Label>
                <Col>
                  <Form.Control type="password" placeholder="Hasło" onChange={e => setPassword(e.target.value)}/>
                </Col>
            </Form.Group>

        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Anuluj
          </Button>
          <Button variant="primary" onClick={handleSubmit}>
            Zaloguj
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default LoginModal