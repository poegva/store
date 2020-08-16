import {connect} from "react-redux";
import Container from "@material-ui/core/Container";
import React from "react";
import ItemsLoading from "../components/ItemsLoading";
import TextBlock from "../components/TextBlock";
import Box from "@material-ui/core/Box";
import Typography from "@material-ui/core/Typography";
import CartItemCard from "../components/CartItemCard";
import {addItem, loadOrder} from "../redux/actions/OrderActions";
import Skeleton from "@material-ui/lab/Skeleton";

function Payment(props) {
    const [loading, setLoading] = React.useState(false);

    React.useEffect(() => {
        if (props.order.status !== 'WAITING_PAYMENT' || !props.order.payment_token || loading)
            return;

        const script = document.createElement("script");
        script.src = "https://kassa.yandex.ru/checkout-ui/v2.js";
        script.async = true;
        script.onload = () => {
            const checkout = new window.YandexCheckout({
                confirmation_token: props.order.payment_token,
                return_url: `http://${window.location.hostname}:3000/order`,
                embedded_3ds: true,
                error_callback(error) {
                    console.log(error);
                    if (error.error === 'token_expired') {
                        setLoading(true);
                        setTimeout(() => props.loadOrder(props.order.id, props.order.token), 2000);
                    }
                }
            });

            checkout.render('payment-form');
        }
        document.body.appendChild(script);
    }, [props.order.payment_token])

    if (props.order.status !== 'WAITING_PAYMENT' || !props.order.payment_token) {
        return null;
    }

    return (
        <Box style={{paddingBottom: 20}}>
            <Typography variant="h5" component="h5" align="center" paragraph>Оплата</Typography>
            {loading ?
                <ItemsLoading variant="h6" loadingText="Обработка оплаты..." /> :
                <div id="payment-form" style={{minHeight: 400}}></div>
            }
        </Box>
    )
}

function OrderDetails(props) {
    return (
        <Box style={{paddingBottom: 20}}>
            <Typography variant="h5" component="h5" align="center" paragraph>Детали</Typography>
            <Typography align="center">Имя: {props.order.name}</Typography>
            <Typography align="center">Телефон: {props.order.phone}</Typography>
            <Typography align="center">Email: {props.order.email}</Typography>
            <Typography align="center">Адрес: {props.order.address.address}</Typography>
        </Box>
    )
}

function OrderContent(props) {
    return (
        <Box style={{paddingBottom: 20}} display="flex" flexDirection="column" justifyContent="center" alignItems="center">
            <Typography variant="h5" component="h5" align="center" paragraph>Товары</Typography>
            <Box display="flex" flexDirection="column" justifyContent="center" style={{width: 500, maxWidth: "100%"}}>
                {props.order.items.map(item => (
                    <CartItemCard quantity={item.quantity} item={item.item} key={item.item.id} />
                ))}
            </Box>
        </Box>
    )
}

function OrderInfo(props) {
    function stateToText(status) {
        switch(status) {
            case 'WAITING_PAYMENT':
                return 'Ожидание оплаты'
            case 'PAYED':
                return 'Оплачен'
            default:
                return status
        }
    }

    return (
        <Box>
            <Typography align="center" paragraph>Статус: {stateToText(props.order.status)}</Typography>
            <Payment order={props.order} loadOrder={props.loadOrder} />
            <OrderDetails order={props.order} />
            <OrderContent order={props.order} />
        </Box>
    )
}

function Order(props) {
    const [error, setError] = React.useState(!props.order.lastOrderId);
    const [reloaded, setReloaded] = React.useState(false);

    const id = props.order.lastOrderId;
    const order = props.order.orders[id];

    React.useEffect(() => {
        if (!error && !id) {
            setError(true);
        } else {
            if (!error) {
                if (!order) {
                    setError(true);
                    console.log("Need to load shit");
                } else {
                    if (!reloaded) {
                        props.loadOrder(id, order.token);
                        setReloaded(true);
                    }
                }
            }
        }
    }, [error, id, props.order.orders]);

    React.useEffect(() => {
        const interval = setInterval(() => {
            if (order) {
                console.log("Reloading order");
                props.loadOrder(id, order.token);
            }
        }, 30000);
        return () => clearInterval(interval);
    }, []);

    let content = null;

    if (error) {
        content = <ItemsLoading error />;
    } else {
        let subContent = null;

        if (!(id in props.order.orders)) {
            subContent = <ItemsLoading />;
        } else {
            subContent = <OrderInfo loadOrder={props.loadOrder} order={props.order.orders[id]} />;
        }

        content = (
            <React.Fragment>
                <TextBlock subtitle={"Заказ №" + id} />
                {subContent}
            </React.Fragment>
        );
    }

    return (
        <Container style={{paddingTop: 20}}>
            {content}
        </Container>
    );
}

const mapStateToProps = store => {
    return {
        order: store.order
    };
}

const mapDispatchToProps = dispatch => {
    return {
        loadOrder: (id, token) => dispatch(loadOrder(id, token))
    };
}

export default connect(
    mapStateToProps,
    mapDispatchToProps
)(Order);