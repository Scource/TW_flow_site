import { withRouter } from "react-router";
import {React, useEffect} from 'react'
import Datetime from "react-datetime";
import axios from 'axios'
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import moment from 'moment'


//dodatkowo sprawdzić czy można elementsform dopisać do elementlistcontainer tak żeby jego logikę też dodac piertro wyzej

const UpdateConn = (props) => {

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
                <Form.Group as={Col} controlId="formEleName">            
                    <Form.Label>Nazwa użytkownika RB</Form.Label>
                    <Form.Control onChange={props.UpdateFunc} name='name' value={props.data.name} type="text" placeholder="Podaj nazwę" />
                </Form.Group>
                <Form.Group as={Col} controlId="formEleCode">            
                    <Form.Label>Kod użytkownika RB</Form.Label>
                    <Form.Control onChange={props.UpdateFunc} name='code' value={props.data.code} type="text" placeholder="Podaj kod" />
                </Form.Group>
            </Form.Row>

            <Form.Row>
                <Form.Group as={Col} controlId="formEleFromDate">            
                    <Form.Label>Data początku obowiązywania</Form.Label>
                    <Datetime onChange={props.updateStartFunc}  value={moment(props.data.dt_from).format('YYYY-MM-DD HH:mm')} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
                <Form.Group as={Col} controlId="formEleToDate">            
                    <Form.Label>Data końca obowiązywania</Form.Label>
                    <Datetime onChange={props.updateEndFunc}  value={moment(props.data.dt_to).format('YYYY-MM-DD HH:mm')} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group as={Col} md={4} controlId="formEleSelectType">
                <Form.Label>Wybierz typ użytkownika</Form.Label>
                <Form.Control name='element_type' value={props.data.element_type} onChange={props.UpdateFunc} 
                 as="select">
                <option>---wybierz typ---</option>
                <option value='0'>POB</option>
                <option value='1'>SE</option>
                </Form.Control>
            </Form.Group>
            </Form.Row>

            <Form.Row>
            <Form.Group>
                <Form.File id="formEleFileInput" label="Dodaj plik" />
            </Form.Group>
            </Form.Row>

            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Button onClick={props.submitFunc} type="submit">Edytuj</Button></Col>
                
            </Form.Row>
        </Form>
    </Container>
    </div>
    )
};


export default withRouter(UpdateConn)