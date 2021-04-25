import {React, useEffect} from 'react'
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import {Link} from 'react-router-dom';
import moment from 'moment'
import axios from 'axios';
import { withRouter } from "react-router";


const  ShowConn = (props) => {

    console.log(props)
    useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        `http://localhost:8000/RB/connection/${props.match.params.id}/edit/`,
      );
      props.setFunc(result.data);
    };
     fetchData();
   }, []);// eslint-disable-line
console.log('AAA', props)
return(
    <Container>
       <h3>Połączenie ID {props.data.pk}</h3>
       <br/>
        <Form>
            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Link to={`${props.prev_match.url}/${props.match.params.id}/edit`}><Button>Edytuj</Button></Link></Col>
            </Form.Row>
            <Form.Row>
            <Form.Group as={Col} controlId="formSelectPOB">
                <Form.Label>Podmiot odpowiedzialny za bilansowanie</Form.Label>
                <Form.Control name='POB' defaultValue={props.data.POB_code} disabled/>
            </Form.Group>

            <Form.Group as={Col} controlId="formSelectSE">
                <Form.Label>Sprzedawca</Form.Label>
                <Form.Control name='SE' defaultValue={props.data.SE_code} disabled/>
            </Form.Group>
            </Form.Row>
            <Form.Row>
                <Form.Group as={Col} controlId="formMeFromDate">            
                    <Form.Label>Data początku </Form.Label>
                    <Form.Control  value={moment(props.data.dt_from).format('YYYY-MM-DD HH:mm')} disabled/>
                </Form.Group>
                <Form.Group as={Col} controlId="formMeToDate">            
                    <Form.Label>Data końca</Form.Label>
                    <Form.Control  value={moment(props.data.dt_to).format('YYYY-MM-DD HH:mm')} disabled/>
                </Form.Group>
            </Form.Row>
        </Form>
    </Container>
    )
};


export default withRouter(ShowConn)