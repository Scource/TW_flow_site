import React from 'react';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import Col from 'react-bootstrap/Col'

function LoginModal(props) {

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
                  <Form.Control placeholder="Nazwa użytkownika"/>
                </Col>
            </Form.Group>
        <Form.Group controlId="formLoginPassword">
                <Form.Label column sm="3">
                  Hasło
                </Form.Label>
                <Col>
                  <Form.Control type="password" placeholder="Hasło"/>
                </Col>
            </Form.Group>

        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Anuluj
          </Button>
          <Button variant="primary" onClick={handleClose}>
            Zaloguj
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default LoginModal