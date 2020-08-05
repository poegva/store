import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import React from "react";
import makeStyles from "@material-ui/core/styles/makeStyles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import MuiPhoneNumber from "material-ui-phone-number";

const useStyles = makeStyles((theme) => ({
    dialogContainer: {
        paddingBottom: theme.spacing(4),
    },
    formContainer: {
        display: "flex",
        flexDirection: "column",
    },
    formInput: {
        paddingBottom: theme.spacing(4),
    },
    dialogGrid: {
        paddingTop: theme.spacing(4),
        paddingBottom: theme.spacing(8),
    },
    itemCard: {
        marginTop: theme.spacing(3),
        display: 'flex',
        justifyContent: 'flex-start'
    },
    itemContent: {
        width: '100%',
    },
    itemImage: {
        width: '100px',
    },
    quantityFlex: {
        display: 'flex'
    },
    submitButton: {
        backgroundColor: "black",
        color: "white",
        '&:hover': {
            backgroundColor: "gray",
        }
    },
}));

export default function ContactForm(props) {
    const classes = useStyles();

    function onNameChange(event) {
        props.setName(event.target.value);
    }

    function onPhoneChange(value) {
        props.setPhone(value);
    }

    function onEmailChange(event) {
        props.setEmail(event.target.value);
    }

    return (
        <Container className={classes.dialogContainer}>
            <Typography component="h5" variant="h5" align="center" className={classes.formInput}>
                Оформить заказ
            </Typography>
            <Container className={classes.formContainer}>
                <TextField
                    id="name"
                    label="Имя"
                    variant="outlined"
                    className={classes.formInput}
                    value={props.order.contacts.name ?? ""}
                    onChange={onNameChange}
                    required
                />
                <MuiPhoneNumber
                    id="phone"
                    label="Телефон"
                    variant="outlined"
                    className={classes.formInput}
                    value={props.order.contacts.phone ?? ""}
                    onChange={onPhoneChange}
                    onlyCountries={['ru']}
                    required
                />
                <TextField
                    id="email"
                    label="Email"
                    variant="outlined"
                    className={classes.formInput}
                    value={props.order.contacts.email ?? ""}
                    onChange={onEmailChange}
                    required
                />
                <Button className={classes.submitButton} onClick={props.submitContacts}>
                    Далее
                </Button>
            </Container>
        </Container>
    );
}