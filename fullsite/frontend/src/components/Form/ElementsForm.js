import {React, useState} from 'react'
import moment from 'moment'
import Datetime from "react-datetime";
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import { withRouter, Redirect } from "react-router";
import axiosConfig from '../../actions/axiosConfig'


const ElementsForm = (props) => {
const [redirect, setRedirect]=useState(false)
const [newElement, setNewElement] =useState({
    code:'', 
    name:'', 
    dt_from:'', 
    dt_to:'', 
    author:1, 
    modified_by:1,
    element_type:''
});

const updateField = e => {
setNewElement({...newElement, [e.target.name]: e.target.value})
};

const updateStartField = event => {
    setNewElement({...newElement, dt_from: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    console.log(event)
};

const updateEndField = event => {
    setNewElement({...newElement, dt_to: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
};

const handleSubmit = event => {
    event.preventDefault();
    axiosConfig.post('/RB/element/create/', newElement)
        .then(res => {
                if (res.status === 201) {
          setRedirect(true)}})
};

if (redirect) {
return <Redirect to={`/element/${(newElement.element_type)==='0' ? 'POB' : 'SE'}`} />
}

return(
    <Container>
    {/* /{redirect ? <Redirect to={`/element/${(newElement.element_type)==='0' ? 'POB' : 'SE'}/`} /> : null} */}
       <h3>Utwórz nowego użytkownika Rynku Bilansującego</h3>
       <br/>
        <Form>
            <Form.Row>
                <Form.Group as={Col} controlId="formEleName">            
                    <Form.Label>Nazwa użytkownika RB</Form.Label>
                    <Form.Control onChange={updateField} name='name' type="text" placeholder="Podaj nazwę" />
                </Form.Group>
                <Form.Group as={Col} controlId="formEleCode">            
                    <Form.Label>Kod użytkownika RB</Form.Label>
                    <Form.Control onChange={updateField} name='code' type="text" placeholder="Podaj kod" />
                </Form.Group>
            </Form.Row>

            <Form.Row>
                <Form.Group as={Col} controlId="formEleFromDate">            
                    <Form.Label>Data początku obowiązywania</Form.Label>
                    <Datetime onChange={updateStartField} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
                <Form.Group as={Col} controlId="formEleToDate">            
                    <Form.Label>Data końca obowiązywania</Form.Label>
                    <Datetime onChange={updateEndField} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group as={Col} md={4} controlId="formEleSelectType">
                <Form.Label>Wybierz typ użytkownika</Form.Label>
                <Form.Control name='element_type' onChange={updateField} 
                as="select">
                <option>---wybierz typ---</option>
                <option value='0'>POB</option>
                <option value='1'>SE</option>
                </Form.Control>
            </Form.Group>
            </Form.Row>
            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Button onClick={handleSubmit} type="submit">Utwórz</Button></Col>
                
            </Form.Row>
        </Form>
    </Container>
    )
};


export default withRouter(ElementsForm)