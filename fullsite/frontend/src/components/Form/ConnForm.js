import {React, useState, useEffect} from 'react'
import Datetime from "react-datetime";
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import axios from 'axios'
import moment from 'moment'


function ConnForm() {
const [newData, setNewData]=useState([])
const [newConn, setNewConn] =useState({
    dt_from:'', 
    dt_to:'', 
    POB:'', 
    SE:'', 
    author:1, 
    modified_by:1 
});



const updateField = e => {
setNewConn({...newConn, [e.target.name]: e.target.value})
console.log(newConn)};

const updateStartField = event => {
    setNewConn({...newConn, dt_from: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    console.log(event)
console.log(newConn)};

const updateEndField = event => {
    setNewConn({...newConn, dt_to: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
console.log(newConn)};

const handleSubmit = event => {
    event.preventDefault();
    console.log(newConn)
    axios.post('http://localhost:8000/RB/connection/create/', newConn)
};

    useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        'http://localhost:8000/RB/element/',
      );
      console.log(result)
      setNewData(result.data);
    };
     fetchData();
  }, []);

return(
    <Container>
       <h3>Utwórz połączenie między elementami</h3>
       <br/>
        <Form>
            <Form.Row>
                <Form.Group as={Col} controlId="formMeFromDate">            
                    <Form.Label>Data początku </Form.Label>
                    <Datetime onChange={updateStartField} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
                <Form.Group as={Col} controlId="formMeToDate">            
                    <Form.Label>Data końca</Form.Label>
                    <Datetime onChange={updateEndField} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group as={Col} controlId="formSelectPOB">
                <Form.Label>Wybierz POB</Form.Label>
                <Form.Control name='POB' onChange={updateField} as="select" htmlSize={7} custom>
                  {newData.filter(el => 
                        el.element_type === 0).map(ele => (
                        <option key={ele.pk} value={ele.pk}>{ele.code}</option>
                    ))}
                </Form.Control>
            </Form.Group>

            <Form.Group as={Col} controlId="formSelectSE">
                <Form.Label>Wybierz SE</Form.Label>
                <Form.Control name='SE' onChange={updateField} as="select" htmlSize={7} custom>
                  {newData.filter(el => 
                        el.element_type === 1).map(ele => (
                        <option key={ele.pk} value={ele.pk}>{ele.code}</option>
                    ))}
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


export default ConnForm