import { withRouter, Redirect } from "react-router";
import {React, useEffect} from 'react'
import Datetime from "react-datetime";
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import moment from 'moment'
import axiosConfig from '../../actions/axiosConfig'

//dodatkowo sprawdzić czy można elementsform dopisać do elementlistcontainer tak żeby jego logikę też dodac piertro wyzej

const UpdateElement = (props) => {

    useEffect(() => {
    const fetchData = async () => {
      const result = await axiosConfig.get(
        `/RB/element/${props.match.params.id}/edit/`,
      );
      props.setFunc(result.data);
    };
     fetchData();
   }, []);// eslint-disable-line

    if (props.redirect) {
       return <Redirect to={`/element/${(props.data.element_type)==='0' ? 'POB' : 'SE'}/${props.match.params.id}/show/`} />
    }

    return(
     <Container>
        <h3>Edytuj użytkownika Rynku Bilansującego</h3>
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
                <Col md={{ span: 2, offset: 11 }}><Button onClick={props.submitFunc} type="submit">Edytuj</Button></Col>
                
            </Form.Row>
        </Form>
    </Container>

    )
};


export default withRouter(UpdateElement)