import {React, useEffect} from 'react'
import Datetime from "react-datetime";
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import ProdConnections from '../ItemList/ProdConnections'
import axios from 'axios'
import moment from 'moment'
import { withRouter } from "react-router";

const UpdateProd = (props) => {

    useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        `http://localhost:8000/RB/powerplant/${props.match.params.id}/edit/`,
      );
      props.setFunc(result.data);
    };
     fetchData();
   }, [])// eslint-disable-line
    console.log(moment(props.data.dt_to).format('YYYY-MM-DD HH:mm'))



return(
    <Container>
       
       <h3>Edytuj wytwórcę</h3>
       <br/>
        <Form>
            <Form.Row>
                <Form.Group as={Col} controlId="formProcName">            
                    <Form.Label>Nazwa wytwórcy</Form.Label>
                    <Form.Control onChange={props.UpdateFunc} defaultValue={props.data.name} name='name' type="text" placeholder="Podaj nazwę" />
                </Form.Group>
                <Form.Group as={Col} controlId="formProdCode">            
                    <Form.Label>Kod PPE</Form.Label>
                    <Form.Control onChange={props.UpdateFunc} defaultValue={props.data.PPE} name='PPE' type="text" placeholder="Podaj kod" />
                </Form.Group>
            </Form.Row>

            <Form.Row>
                <Form.Group as={Col} controlId="formProdFromDate">            
                    <Form.Label>Data początku bilansowania</Form.Label>
                    <Datetime  onChange={props.updateStartFunc} value={moment(props.data.dt_from).format('YYYY-MM-DD HH:mm')} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
                <Form.Group as={Col} controlId="formProdToDate">            
                    <Form.Label>Data końca bilansowania</Form.Label>
                    <Datetime onChange={props.updateEndFunc} value={moment(props.data.dt_from).format('YYYY-MM-DD HH:mm')} dateFormat="YYYY-MM-DD" timeFormat="HH:mm" />
                </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group  as={Col} md={4} controlId="formProdSelectType">
                <Form.Label>Wybierz typ</Form.Label>
                <Form.Control as="select" name='element_type' onChange={props.UpdateFunc} value={props.data.element_type}>
                <option>---wybierz typ---</option>
                <option value='0'>Wytw</option>
                <option value='1'>Mikro</option>
                <option value='2'>Prosument</option>

                </Form.Control>
            </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group>
                <Form.File id="formProdFileInput" label="Dodaj plik" />
            </Form.Group>
            </Form.Row>

            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Button onClick={props.submitFunc} type="submit">Edytuj</Button></Col>
                
            </Form.Row>
        </Form>

        <ProdConnections />
    </Container>
    )
};


export default withRouter(UpdateProd)