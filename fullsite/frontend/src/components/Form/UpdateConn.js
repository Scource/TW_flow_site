import {React, useEffect} from 'react'
import Datetime from "react-datetime";
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import moment from 'moment'
import { withRouter, Redirect } from "react-router";
import axiosConfig from '../../actions/axiosConfig'

const  UpdateConn = (props) => {

    useEffect(() => {
    const fetchData = async () => {
      const result = await axiosConfig.get(
        `/RB/connection/${props.match.params.id}/edit/`,
      );
      props.setFunc(result.data);
    };
     fetchData();
   }, [])// eslint-disable-line

   if (props.redirectUpdate) {
       return <Redirect to={`/connections/${props.match.params.id}/show/`} />

   }

return(
    <Container>
        <h3>Edytuj połączenie między elementami</h3>
       <br/>
        <Form>
            <Form.Row>
                <Form.Group as={Col} controlId="formMeFromDate">            
                    <Form.Label>Data początku </Form.Label>
                    <Datetime onChange={props.updateStartFunc} value={moment(props.data.dt_from).format('YYYY-MM-DD HH:mm')} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
                <Form.Group as={Col} controlId="formMeToDate">            
                    <Form.Label>Data końca</Form.Label>
                    <Datetime onChange={props.updateEndFunc} value={moment(props.data.dt_to).format('YYYY-MM-DD HH:mm')} dateFormat="YYYY-MM-DD" timeFormat="HH:mm"/>
                </Form.Group>
            </Form.Row>

            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Button onClick={props.submitFunc} type="submit">Edytuj</Button></Col>
            </Form.Row>
        </Form>
    </Container>
    )
};


export default withRouter(UpdateConn)