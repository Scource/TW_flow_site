import { withRouter, Redirect } from "react-router";
import {React, useEffect} from 'react'
import axiosConfig from '../../actions/axiosConfig'
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
      const result = await axiosConfig.get(
        `/RB/element/${props.match.params.id}/edit/`,
      );
      props.setFunc(result.data);
    };
     fetchData();
   }, []);// eslint-disable-line

    if (props.redirectDelete) {        
       return <Redirect to={`${props.prev_match.url}`} />
    }

    return(
    <Container>
       <h3>Użytkownik Rynku Bilansującego</h3>
       <br/>
        <Form>
            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}>
                    <Link to={`${props.prev_match.url}/${props.match.params.id}/edit`} className="btn btn-primary">Edytuj</Link>
                    <Button onClick={() => {if (window.confirm('Are you sure you wish to delete this item?')) {props.delFunc(props.match.params.id)}}}>Usuń</Button>
                </Col>

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
    )
};


export default withRouter(ShowElement)