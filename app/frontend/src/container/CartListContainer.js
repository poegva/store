import React from "react";
import {connect} from "react-redux";
import CartList from "../components/CartList";
import {addItem, removeItem, setItem} from "../actions/CartActions";


const mapStateToProps = store => {
    return {
        cart: store.cart,
    };
}

const mapDispatchToProps = dispatch => {
    return {
        addItem: item => dispatch(addItem(item)),
        removeItem: item => dispatch(removeItem(item)),
        setItem: (item, quantity) => dispatch(setItem(item, quantity)),
    };
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(CartList);