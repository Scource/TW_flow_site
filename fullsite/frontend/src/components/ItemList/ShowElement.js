import { withRouter } from "react-router";
import {React, useEffect} from 'react'
import axios from 'axios'
import Form from 'react-bootstrap/Form';
import {Link} from 'react-router-dom';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import moment from 'moment'
import ElementConnections from './ElementConnections'

const ShowElement = (props) => {

    useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        `http://localhost:8000/RB/element/${props.match.params.id}/edit/`,
      );
      props.setFunc(result.data);
    };
     fetchData();
   }, []);// eslint-disable-line

    return(
        <div>
 
    <Container>
       <h3>Edytuj użytkownika Rynku Bilansującego</h3>
       <br/>
        <Form>
            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Link to={`${props.prev_match.url}/${props.match.params.id}/edit`}><Button>Edytuj</Button></Link></Col>

            </Form.Row>
            <Form.Row>
                <Form.Group as={Col} controlId="formEleName">            
                    <Form.Label>Nazwa użytkownika RB</Form.Label>
                    <Form.Control name='name' defaultValue={props.data.name} type="text" placeholder="Podaj nazwę" disabled/>
                </Form.Group>
                <Form.Group as={Col} controlId="formEleCode">            
                    <Form.Label>Kod użytkownika RB</Form.Label>
                    <Form.Control name='code' defaultValue={props.data.code} type="text" placeholder="Podaj kod" disabled/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
                <Form.Group as={Col} controlId="formEleFromDate">            
                    <Form.Label>Data początku obowiązywania</Form.Label>
                    <Form.Control value={moment(props.data.dt_from).format('YYYY-MM-DD HH:mm')} disabled/>
                </Form.Group>
                <Form.Group as={Col} controlId="formEleToDate">            
                    <Form.Label>Data końca obowiązywania</Form.Label>
                    <Form.Control value={moment(props.data.dt_to).format('YYYY-MM-DD HH:mm')} disabled/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group as={Col} md={4} controlId="formEleSelectType">
                <Form.Label>Typ użytkownika</Form.Label>
                <Form.Control name='element_type' defaultValue= {props.data.element_type ? 'SE' : 'POB'} disabled />
                    
            </Form.Group>
            </Form.Row>
        </Form>

    <ElementConnections pk={props.data.pk}/>    
    </Container>
    </div>
    )
};


export default withRouter(ShowElement)