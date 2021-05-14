import {React, useEffect} from 'react'
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import {Link} from 'react-router-dom';
import moment from 'moment'
import { withRouter, Redirect } from "react-router";
import axiosConfig from '../../actions/axiosConfig'

const  ShowConn = (props) => {

    useEffect(() => {
    const fetchData = async () => {
      const result = await axiosConfig.get(
        `/RB/connection/${props.match.params.id}/edit/`,
      );
      props.setFunc(result.data);
    };
     fetchData();
   }, []);// eslint-disable-line

   if (props.redirectDelete) {
       return <Redirect to="/connections" />
   }

return(
    <Container>
        <h3>Połączenie ID {props.data.pk}</h3>
       <br/>
        <Form>
            <Form.Row>
                <Col md={{ span: 2, offset: 11 }}><Link to={`${props.prev_match.url}/${props.match.params.id}/edit`}>
                    <Button>Edytuj</Button></Link>
                <Button onClick={() => {if (window.confirm('Are you sure you wish to delete this item?')) {props.delFunc(props.match.params.id)}}}>Usuń</Button>
                </Col>
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