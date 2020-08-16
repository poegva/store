import {
    returnToContacts,
    setAddress,
    setDeliverySelected,
    submitOrder
} from "../redux/actions/OrderActions";
import {connect} from "react-redux";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import GenericForm from "../components/form/GenericForm";
import React from "react";
import AddressField from "../components/form/AddressField";
import DeliveryOptionField from "../components/form/DeliveryOptionField";
import {useHistory} from "react-router-dom";

function DeliveryForm(props) {
    let history = useHistory();

    function convertItemToData(item) {
        return {
            item: item.item.id,
            quantity: item.quantity,
        };
    }

    function submitOrder() {
        const orderData = {
            name: props.order.contacts.name,
            email: props.order.contacts.email,
            phone: props.order.contacts.phone,
            address: props.order.address,
            delivery_option: props.order.delivery.selected,
            items: Object.values(props.order.cart).map(item => convertItemToData(item))
        };

        props.submitOrder(orderData, () => history.push('/order'));
    }

    return (
        <Container style={{paddingTop: 20, paddingBottom: 20}}>
            <Typography component="h5" variant="h5" align="center" style={{paddingBottom: 40}}>
                Данные доставки
            </Typography>
            <GenericForm submit={submitOrder} returnBack={props.returnToContacts}>
                <AddressField
                    id="address"
                    label="Адрес"
                    value={props.order.address}
                    setValue={props.setAddress}
                    required
                />
                <DeliveryOptionField
                    id="options"
                    label="Способ доставки"
                    value={props.order.delivery.selected}
                    setValue={props.setDeliverySelected}
                    options={props.order.delivery.options}
                    required
                />
            </GenericForm>
        </Container>
    );
}

const mapStateToProps = store => {
    return {
        order: store.order,
    };
}

const mapDispatchToProps = dispatch => {
    return {
        returnToContacts: () => dispatch(returnToContacts()),
        setAddress: (address) => dispatch(setAddress(address)),
        setDeliverySelected: (selected) => dispatch(setDeliverySelected(selected)),
        submitOrder: (orderData, redirect) => dispatch(submitOrder(orderData, redirect)),
    };
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(DeliveryForm);