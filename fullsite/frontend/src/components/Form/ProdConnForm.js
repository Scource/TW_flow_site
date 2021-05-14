import {React, useState, useEffect} from 'react'
import Datetime from "react-datetime";
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import moment from 'moment';
import { withRouter, Redirect} from "react-router";
import axiosConfig from '../../actions/axiosConfig'

const  ProdConnForm =(props) => {
console.log(props)
const [redirect, setRedirect]=useState(false)
const [POBList, setPOBList]=useState([])
const [newConn, setNewConn] =useState({
    dt_from:'', 
    dt_to:'', 
    POB:'', 
    PowerPlantItem: props.data.pk, 
    author:1, 
    modified_by:1,
    element_type: 1
});

const updateField = e => {
setNewConn({...newConn, [e.target.name]: e.target.value})
};

const updateStartField = event => {
    setNewConn({...newConn, dt_from: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
    };

const updateEndField = event => {
    setNewConn({...newConn, dt_to: moment(event._d).format('YYYY-MM-DD HH:mm') }); 
};

const handleSubmit = event => {
    event.preventDefault();
    console.log(newConn)
    axiosConfig.post('/RB/powerplant/connection/create/', newConn)
        .then(res => {
                if (res.status === 201) {
          setRedirect(true)}})
};

    useEffect(() => {
    const fetchPOB = async () => {
      const result = await axiosConfig.get(
        `/RB/element/POB/`,
      );
      setPOBList(result.data);
    };
     fetchPOB();

  }, []);


if (redirect) {
return <Redirect to={`/producers/${props.data.pk}/show`} />
}

return(
    <Container>
       <h3>Utwórz połączenie do POB</h3>
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
                  {POBList.filter(el => 
                        el.element_type === 0).map(ele => (
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


export default withRouter(ProdConnForm)