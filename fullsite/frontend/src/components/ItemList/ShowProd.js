import {React, useEffect} from 'react'
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import ProdConnections from './ProdConnections'
import axios from 'axios'
import moment from 'moment'
import { withRouter} from "react-router";
import {Link} from 'react-router-dom';

const ShowProd = (props) => {


    useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        `http://localhost:8000/RB/powerplant/${props.match.params.id}/edit/`,
      );
      props.setFunc(result.data);
    };
     fetchData();
   }, [])// eslint-disable-line

return(
    <Container>
       
       <h3>{props.data.name}</h3>
        <Form style={{marginBottom: '40px'}}>
            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Link to={`${props.prev_match.url}/${props.match.params.id}/edit`}><Button>Edytuj</Button></Link></Col>
                
            </Form.Row>
            <Form.Row>
                <Form.Group as={Col} controlId="formProcName">            
                    <Form.Label>Nazwa wytwórcy</Form.Label>
                    <Form.Control defaultValue={props.data.name} name='name' type="text" disabled />
                </Form.Group>
                <Form.Group as={Col} controlId="formProdCode">            
                    <Form.Label>Kod PPE</Form.Label>
                    <Form.Control defaultValue={props.data.PPE} name='PPE' type="text" disabled/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
                <Form.Group as={Col} controlId="formProdFromDate">            
                    <Form.Label>Data początku bilansowania</Form.Label>
                    <Form.Control  value={moment(props.data.dt_from).format('YYYY-MM-DD HH:mm')} disabled/>
                </Form.Group>
                <Form.Group as={Col} controlId="formProdToDate">            
                    <Form.Label>Data końca bilansowania</Form.Label>
                    <Form.Control value={moment(props.data.dt_from).format('YYYY-MM-DD HH:mm')} disabled/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group  as={Col} md={4} controlId="formProdSelectType">
                <Form.Label>Typ Wytwórcy</Form.Label>
                <Form.Control name='element_type' value={props.data.element_type===0 ? "Wytwórca" 
                : props.data.element_type ===1 ? "Mikroinstalacja" : "Prosument"} disabled>
                </Form.Control>
            </Form.Group>
            </Form.Row>
        </Form>

        <ProdConnections />
    </Container>
    )
};


export default withRouter(ShowProd)